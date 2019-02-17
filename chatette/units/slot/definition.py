from copy import deepcopy

from chatette.units import Example, UnitDefinition, randomly_change_case, \
                           ENTITY_MARKER, with_leading_lower, with_leading_upper
from chatette.utils import choose
from .rule_content import DummySlotValRuleContent


class SlotDefinition(UnitDefinition):
    """
    This class represents the definition of a slot,
    containing all the rules that it could generate.
    """

    def __init__(self, name, modifiers, rules=None):
        super(SlotDefinition, self).__init__(name, modifiers, rules=rules)
        self.type = "slot"
        self.arg_values_encountered = []

    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of the rules at random and
        returns the string generated and the entities inside it as a dict.
        This is the only kind of definition that will generate an entity.
        """
        # (str, str) -> {"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}
        if (arg_value is not None
                and arg_value not in self.arg_values_encountered):
            # Memorize arg value
            self.arg_values_encountered.append(arg_value)

        chosen_rule = None
        if variation_name is None:
            chosen_rule = choose(self.rules)
        else:
            if variation_name not in self.variations:
                raise SyntaxError("Couldn't find a variation named '" +
                                  variation_name + "' for " + self.type + " '" + self.name + "'")
            chosen_rule = choose(self.variations[variation_name])

        if chosen_rule is None:  # No rule
            return Example()

        if len(chosen_rule) <= 0:
            raise ValueError("Tried to generate an entity using an empty rule " +
                             "for slot named '" + self.name + "'")

        generated_example = Example()
        for token in chosen_rule:
            generated_token = token.generate_random()
            generated_example.text += generated_token.text
            generated_example.entities.extend(generated_token.entities)

        if self.modifiers.casegen and self.can_have_casegen():
            generated_example.text = randomly_change_case(generated_example.text)

        # Replace `arg` inside the generated sentence
        generated_example.text = ENTITY_MARKER + \
            self._replace_arg(generated_example.text, arg_value).strip()  # Strip for safety

        # Add the entity in the list
        slot_value = chosen_rule[0].name
        if not isinstance(chosen_rule[0], DummySlotValRuleContent):
            slot_value = generated_example.text[len(ENTITY_MARKER):]
        # Replace the argument by its value if needed
        slot_value = self._replace_arg(slot_value, arg_value)
        generated_example.entities.append({
            "slot-name": self.name,
            "text": generated_example.text[len(ENTITY_MARKER):],
            "value": slot_value,
        })

        return generated_example

    def generate_all(self, variation_name=None, arg_value=None):
        if (arg_value is not None
                and arg_value not in self.arg_values_encountered):
            # Memorize arg value
            self.arg_values_encountered.append(arg_value)

        generated_examples = []

        relevant_rules = self.rules
        if variation_name is not None:
            if variation_name in self.variations:
                relevant_rules = self.variations[variation_name]
            else:
                raise SyntaxError("Couldn't find variation '" +
                                  str(variation_name) + "' for slot '" +
                                  str(self.name) + "'")

        if not relevant_rules:  # No rules
            if variation_name is None:
                raise SyntaxError("No rules could be found for "+self.type+" '"+
                                self.name+"'")
            else:
                raise SyntaxError("No rules could be found for "+self.type+" '"+
                                self.name+"' (variation: '"+variation_name+"'")

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
                            tmp_buffer.append(
                                Example(
                                    ex.text + possibility.text,
                                    ex.entities + possibility.entities,  # this is a list
                                )
                            )
                    examples_from_current_rule = tmp_buffer

            # Replace `arg` inside generated sentences
            if arg_value is not None and self.modifiers.argument_name is not None:
                for ex in examples_from_current_rule:
                    ex.text = self._replace_arg(ex.text, arg_value)
                    for entity in ex.entities:
                        entity["text"] = self._replace_arg(entity["text"],
                                                           arg_value)
                        entity["value"] = self._replace_arg(entity["value"],
                                                            arg_value)

            # Apply casegen
            if self.modifiers.casegen and self.can_have_casegen():
                tmp_examples = []
                for ex in examples_from_current_rule:
                    (lower_ex, upper_ex) = (deepcopy(ex), deepcopy(ex))
                    lower_ex.text = with_leading_lower(lower_ex.text)
                    upper_ex.text = with_leading_upper(upper_ex.text)
                    if lower_ex != upper_ex:
                        tmp_examples.append(lower_ex)
                        tmp_examples.append(upper_ex)
                    else:
                        tmp_examples.append(ex)
                examples_from_current_rule = tmp_examples

            # Add the entity in the list
            slot_value = rule[0].name
            if not isinstance(rule[0], DummySlotValRuleContent):
                slot_value = None
            else:  # Replace the argument by its value if needed
                slot_value = self._replace_arg(slot_value, arg_value)
            for ex in examples_from_current_rule:
                if slot_value is not None:
                    ex.entities.append({
                        "slot-name": self.name,
                        "text": ex.text[:],
                        "value": slot_value,
                    })
                else:
                    ex.entities.append({
                        "slot-name": self.name,
                        "text": ex.text[:],
                        "value": ex.text[:],
                    })

            generated_examples.extend(examples_from_current_rule)

        for ex in generated_examples:
            ex.text = ENTITY_MARKER + ex.text

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
                        text = example.text
                        if text in synonyms:
                            synonyms[text].append(text)
                        else:
                            synonyms[text] = [text]
                continue

            current_examples = []
            for token in rule:
                current_token_all_generations = token.generate_all()
                if len(current_examples) <= 0:
                    current_examples = [gen.text
                                        for gen in current_token_all_generations]
                else:
                    current_examples = [example_part + gen.text
                                        for example_part in current_examples
                                        for gen in current_token_all_generations]

            if slot_value not in synonyms:
                synonyms[slot_value] = current_examples
            else:
                synonyms[slot_value].extend(current_examples)

        if self.modifiers.argument_name is not None:
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
        if arg_value is not None and self.modifiers.argument_name is not None:
            text = self.arg_regex.sub(arg_value, text)
            text = text.replace(r"\$", "$")
        return text

    def _contains_arg(self, text):
        """
        Checks whether `text` contains at least once the argument identifier
        (and if it is marked as 'to replace').
        @pre: `self.arg_regex` is not `None`
        """
        # (str) -> (bool)
        return self.arg_regex.search(text) is not None


    def _get_template_decl(self, variation=None):
        return '@' + super(SlotDefinition, self)._get_template_decl(variation)
    def _get_template_rules(self, variation=None):
        rules = self.rules
        if variation is not None:
            rules = self.variations[variation]
        rule_templates = []
        for rule in rules:
            alt_slot_val = None
            if isinstance(rule[0], DummySlotValRuleContent):
                alt_slot_val = rule[0].name
            rule_templates.append(''.join([sub_rule.as_string()
                                           for sub_rule in rule]))
            if alt_slot_val is not None:
                rule_templates[-1] += " = " + alt_slot_val
        return rule_templates

    # Everything else is in the superclass
