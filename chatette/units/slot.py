#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .units import *
try:
   from chatette.parser_utils import remove_escapement
   from chatette.utils import choose
except ImportError:
   from parser_utils import remove_escapement
   from utils import choose


class SlotDefinition(UnitDefinition):
    """
    This class represents the definition of a slot,
    containing all the rules that it could generate.
    """
    def __init__(self, name, rules=[], arg=None, casegen=False):
        super(SlotDefinition, self).__init__(name, rules=rules, arg=arg,
            casegen=casegen)
        self.type = "alias"
        self.arg_values_encountered = []


    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of your rule at random and
        returns the string generated and the entities inside it as a dict.
        This is the only kind of definition that will generate an entity.
        """
        # (str, str) -> {"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}
        if (    arg_value is not None
            and arg_value not in self.arg_values_encountered):
            # Memorize arg value
            self.arg_values_encountered.append(arg_value)

        chosen_rule = None
        if variation_name is None:
            chosen_rule = choose(self.rules)
        else:
            if variation_name not in self.variations:
                raise SyntaxError("Couldn't find a variation named '"+
                    variation_name+"' for "+self.type+" '"+self.name+"'")
            chosen_rule = choose(self.variations[variation_name])

        if chosen_rule is None:  # No rule
            return EMPTY_GEN()

        if len(chosen_rule) <= 0:
            raise ValueError("Tried to generate an entity using an empty rule "+
                "for slot named '"+self.name+"'")

        generated_example = EMPTY_GEN()
        for token in chosen_rule:
            generated_token = token.generate_random()
            generated_example["text"] += generated_token["text"]
            generated_example["entities"].extend(generated_token["entities"])

        if self.casegen:
            generated_example["text"] = randomly_change_case(generated_example["text"])

        # Replace `arg` inside the generated sentence
        generated_example["text"] = \
            self._replace_arg(generated_example["text"], arg_value).strip()  # Strip for safety

        # Add the entity in the list
        slot_value = chosen_rule[0].name
        if not isinstance(chosen_rule[0], DummySlotValRuleContent):
            slot_value = generated_example["text"][:]
        # Replace the argument by its value if needed
        slot_value = self._replace_arg(slot_value, arg_value)
        generated_example["entities"].append({
            "slot-name": self.name,
            "text": generated_example["text"][:],
            "value": slot_value,
        })

        return generated_example

    def generate_all(self, variation_name=None, arg_value=None):
        if (    arg_value is not None
            and arg_value not in self.arg_values_encountered):
            # Memorize arg value
            self.arg_values_encountered.append(arg_value)

        generated_examples = []

        relevant_rules = self.rules
        if variation_name is not None:
            if variation_name in self.variations:
                relevant_rules = self.variations[variation_name]
            else:
                raise SyntaxError("Couldn't find variation '"+
                                  str(variation_name)+"' for slot '"+
                                  str(self.name)+"'")

        for rule in relevant_rules:
            examples_from_current_rule = []
            for sub_unit_rule in rule:
                sub_unit_possibilities = \
                    sub_unit_rule.generate_all()
                if len(examples_from_current_rule) <= 0:
                    examples_from_current_rule = sub_unit_possibilities
                else:
                    tmp_buffer = []
                    for ex in examples_from_current_rule:
                        for possibility in sub_unit_possibilities:
                            tmp_buffer.append({
                                "text": ex["text"]+possibility["text"],
                                "entities": ex["entities"]+possibility["entities"],
                            })
                    examples_from_current_rule = tmp_buffer

            # Replace `arg` inside generated sentences
            if arg_value is not None and self.argument_identifier is not None:
                for ex in examples_from_current_rule:
                    ex["text"] = self._replace_arg(ex["text"], arg_value)
                    for entity in ex["entities"]:
                        entity["text"] = self._replace_arg(entity["text"],
                                                           arg_value)
                        entity["value"] = self._replace_arg(entity["value"],
                                                            arg_value)

            # Add the entity in the list
            slot_value = rule[0].name
            if not isinstance(rule[0], DummySlotValRuleContent):
                slot_value = None
            else:  # Replace the argument by its value if needed
                slot_value = self._replace_arg(slot_value, arg_value)
            for ex in examples_from_current_rule:
                if slot_value is not None:
                    ex["entities"].append({
                        "slot-name": self.name,
                        "text": ex["text"][:],
                        "value": slot_value,
                    })
                else:
                    ex["entities"].append({
                        "slot-name": self.name,
                        "text": ex["text"][:],
                        "value": ex["text"][:],
                    })

            generated_examples.extend(examples_from_current_rule)

        return generated_examples


    def get_synonyms_dict(self):
        """
        Makes a dict of the synonyms for entities
        based on the slot values they are assigned.
        """
        # () -> ({str: [str]})
        synonyms = dict()
        for rule in self.rules:
            slot_value = rule[0].name
            if not isinstance(rule[0], DummySlotValRuleContent):
                for token in rule:
                    current_examples = token.generate_all()
                    for example in current_examples:
                        text = example["text"]
                        if text in synonyms:
                            synonyms[text].append(text)
                        else:
                            synonyms[text] = [text]
                continue

            current_examples = []
            for token in rule:
                current_token_all_generations = token.generate_all()
                if len(current_examples) <= 0:
                    current_examples = [gen["text"]
                                       for gen in current_token_all_generations]
                else:
                    current_examples = [example_part+gen["text"]
                                        for example_part in current_examples
                                        for gen in current_token_all_generations]

            if slot_value not in synonyms:
                synonyms[slot_value] = current_examples
            else:
                synonyms[slot_value].extend(current_examples)

        if self.argument_identifier is not None:
            (unprocessed_synonyms, synonyms) = (synonyms, dict())
            # Manage arguments
            for slot_value in unprocessed_synonyms:
                if self._contains_arg(slot_value):
                    for arg_value in self.arg_values_encountered:
                        processed_slot_val = \
                            self._replace_arg(slot_value, arg_value)
                        synonyms[processed_slot_val] = []
                        for ex in unprocessed_synonyms[slot_value]:
                            if self._contains_arg(ex):
                                for arg_value in self.arg_values_encountered:
                                    synonyms[processed_slot_val].append(
                                        self._replace_arg(ex, arg_value)
                                    )
                            else:
                                synonyms[processed_slot_val].append(ex)
                else:
                    synonyms[slot_value] = []
                    for ex in unprocessed_synonyms[slot_value]:
                        if self._contains_arg(ex):
                            for arg_value in self.arg_values_encountered:
                                synonyms[slot_value].append(
                                    self._replace_arg(ex, arg_value)
                                )
                        else:
                            synonyms[slot_value].append(ex)

        return synonyms


    def _replace_arg(self, text, arg_value):
        """If needed, replaces the arguments by their value in `text`."""
        # (str, str) -> (str)
        if arg_value is not None and self.argument_identifier is not None:
            text = self.arg_regex.sub(arg_value, text)
            text = text.replace("\$", "$")
        return text

    def _contains_arg(self, text):
        """
        Checks whether `text` contains at least once the argument identifier
        (and if it is marked as 'to replace').
        @pre: `self.arg_regex` is not `None`
        """
        # (str) -> (bool)
        return (self.arg_regex.search(text) is not None)

    # Everything else is in the superclass


class SlotRuleContent(RuleContent):
    """
    This class represents a slot as it can be contained in a rule,
    with its modifiers.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: int
        - arg: str
        - variation-name: str
        - slot-val: str (to define later)
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            super(SlotRuleContent, self).__init__(name, leading_space=leading_space,
                variation_name=variation_name, arg_value=arg_value, casegen=casegen,
                randgen=randgen, percentage_gen=percentage_gen, parser=parser)
            self.casegen_checked = False

    def can_have_casegen(self):
        return self.parser.get_definition(self.name, Unit.slot) \
                          .can_have_casegen()
    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True


    def generate_random(self, generated_randgens=dict()):
        self.check_casegen()

        # Manage randgen
        if self.randgen is not None and self.randgen in generated_randgens:
            if generated_randgens[self.randgen]:
                pass  # Must be generated
            else:
                return EMPTY_GEN()  # Cannot be generated
        elif self.randgen is not None:
            if randint(0,99) >= self.percentgen:
                # Don't generated this randgen
                if self.randgen != "":
                    generated_randgens[self.randgen] = False
                return EMPTY_GEN()
            elif self.randgen != "":
                # Generate this randgen
                generated_randgens[self.randgen] = True

        generated_example = self.parser.get_definition(self.name, Unit.slot)\
                                       .generate_random(self.variation_name, \
                                                        self.arg_value)

        if self.casegen:
            generated_example["text"] = \
                randomly_change_case(generated_example["text"])
        if self.leading_space and may_get_leading_space(generated_example["text"]):
            generated_example["text"] = ' '+generated_example["text"]
        return generated_example

    def generate_all(self):
        self.check_casegen()

        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(EMPTY_GEN())

        generated_examples.extend(self.parser \
                                        .get_definition(self.name, Unit.slot) \
                                        .generate_all(self.variation_name,
                                                      self.arg_value))

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex["text"]):
                    generated_examples[i]["text"] = ' '+ex["text"]
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                tmp_buffer.append({
                    "text": with_leading_lower(ex["text"]),
                    "entities": ex["entities"],
                })
                tmp_buffer.append({
                    "text": with_leading_upper(ex["text"]),
                    "entities": ex["entities"],
                })
            generated_examples = tmp_buffer
        return generated_examples

    def get_nb_possible_generated_examples(self):
        nb_possible_ex = self.parser.get_definition(self.name, Unit.slot) \
                                    .get_nb_possible_generated_examples(self.variation_name)

        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex


class DummySlotValRuleContent(RuleContent):
    """
    This class is supposed to be the first rule inside a list of rules that has
    a slot value. It won't generate anything ever.
    `self.name` and `self.slot_value` map to the slot value it represents.
    """
    def __init__(self, name, next_token):
        # (str, RuleContent) -> ()
        self.name = remove_escapement(name)
        self.slot_value = self.name
        self.real_first_token = next_token

    def can_have_casegen(self):
        return self.real_first_token.can_have_casegen()


    def generate_random(self):
        return EMPTY_GEN()

    def generate_all(self):
        return [EMPTY_GEN()]


    def printDBG(self, nb_indent=0):
        indentation = nb_indent*'\t'
        print(indentation+"Slot val: "+self.name)
