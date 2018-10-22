#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint

from .units import *
try:
   from chatette.utils import choose
except ImportError:
   from utils import choose


class ChoiceContent(RuleContent):
    """
    This class represents a choice as it can be contained in a rule,
    with its modifiers.
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        # TODO: maybe more?
    """
    def __init__(self, name, leading_space=False, variation_name=None,
        arg_value=None, casegen=False, randgen=None, percentage_gen=None,
        parser=None):
            # NOTE: its name would be the unparsed text as a string
            if randgen is not None and randgen != "":
                raise SyntaxError("Choices cannot have a named randgen, "+
                    "as was the case for '"+name+"': "+randgen+" ('?' unescaped?)")
            if variation_name is not None:
                raise SyntaxError("Choices cannot have a variation, as was the "+
                    "case for '"+name+"' ('#' unescaped?)")  # TODO: change the symbol to a variable from parser_utils
            if arg_value is not None:
                raise SyntaxError("Choices cannot have an argument, as was the "+
                    "case for '"+name+"' ('$' unescaped?)")
            if percentage_gen is not None:
                raise SyntaxError("Choices cannot have an percentage for random"+
                    "generation, as was the case for '"+name+"' ('/' unescaped?)")

            super(ChoiceContent, self).__init__(name,
                                                leading_space=leading_space,
                                                variation_name=None,
                                                arg_value=None,
                                                casegen=casegen,
                                                randgen=randgen,
                                                percentage_gen=None,
                                                parser=None)
            self.choices = []
            self.casegen_checked = False

    def can_have_casegen(self):
        for choice in self.choices:
            if len(choice) > 0 and choice[0].can_have_casegen():
                return True
        return False
    def check_casegen(self):
        """Checks that casegen is applicable (at generation time)."""
        if not self.casegen_checked and self.casegen:
            if not self.can_have_casegen():
                self.casegen = False
            self.casegen_checked = True


    def add_choice(self, choice):
        # (RuleContent) -> ()
        if len(choice) <= 0:
            return
        self.choices.append(choice)
    def add_choices(self, choices):
        # ([RuleContent]) -> ()
        interesting_choices = [choice for choice in choices if len(choice) > 0]
        if len(interesting_choices) <= 0:
            return
        self.choices.extend(interesting_choices)


    def generate_random(self, generated_randgens=dict()):
        self.check_casegen()

        # Manage randgen
        if self.randgen is not None and randint(0,99) >= self.percentgen:
            return EMPTY_GEN()
        if len(self.choices) <= 0:
            return EMPTY_GEN

        choice = choose(self.choices)
        generated_example = EMPTY_GEN()
        for token in choice:
            generated_token = token.generate_random(generated_randgens)
            generated_example["text"] += generated_token["text"]
            generated_example["entities"].extend(generated_token["entities"])

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

        for choice in self.choices:
            current_examples = []
            for token in choice:
                current_token_all_generations = token.generate_all()
                if len(current_examples) <= 0:
                    current_examples = [gen
                                        for gen in current_token_all_generations]
                else:
                    current_examples = [{
                                            "text": partial_example["text"]+gen["text"],
                                            "entities": partial_example["entities"]+gen["entities"],
                                        }
                                        for partial_example in current_examples
                                        for gen in current_token_all_generations]
            generated_examples.extend(current_examples)

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
        return generated_examples

    def get_nb_possible_generated_examples(self):
        nb_possible_ex = 0
        for choice in self.choices:
            choice_nb_ex = 0
            for token in choice:
                current_nb_ex = token.get_nb_possible_generated_examples()
                if choice_nb_ex == 0:
                    choice_nb_ex = current_nb_ex
                else:
                    choice_nb_ex *= current_nb_ex
            nb_possible_ex += choice_nb_ex

        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex


    def printDBG(self, nb_indent=0):
        indentation = nb_indent*'\t'
        print(indentation+self.name)
        print(indentation+"\tvariation name: "+str(self.variation_name))
        print(indentation+"\targ value: "+str(self.arg_value))
        print(indentation+"\tcasegen: "+str(self.casegen))
        print(indentation+"\trandgen: "+str(self.randgen)+" with percentage: "
            +str(self.percentgen))

        for choice in self.choices:
            print(indentation+"\tChoice:")
            for token in choice:
                token.printDBG(nb_indent+2)
