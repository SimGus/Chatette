#!/usr/bin/env python3

from random import randint

from .units import *


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

    def add_choice(self, choice):
        # (RuleContent) -> ()
        self.choices.append(choice)
    def add_choices(self, choices):
        # ([RuleContent]) -> ()
        self.choices.extend(choices)


    def generate_random(self, generated_randgens=dict()):
        # Manage randgen
        if self.randgen is not None and randint(0,99) >= self.percentgen:
            return EMPTY_GEN()
        if len(self.choices) <= 0:
            return EMPTY_GEN

        choice = self.choices[randint(0,len(self.choices)-1)]
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
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append(EMPTY_GEN())

        for choice in self.choices:
            generated_examples.extend(choice.generate_all())

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex):
                    generated_examples[i]["text"] = ' '+ex["text"]
        if self.casegen:
            tmp_buffer = []
            for ex in generated_examples:
                tmp.buffer.append({
                    "text": with_leading_lower(ex["text"]),
                    "entities": ex["entities"],
                })
                tmp.buffer.append({
                    "text": with_leading_upper(ex["text"]),
                    "entities": ex["entities"],
                })
        return generated_examples


    def printDBG(self, nb_indent):
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
