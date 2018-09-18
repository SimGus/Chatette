#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint

from .units import *


class WordRuleContent(RuleContent):
    """
    Represents a word inside a rule
    Accepted modifiers:
        - leading-space: bool
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=None, parser=None):
            if variation_name is not None:
                raise SyntaxError("Words cannot have variations, yet '"+
                    name+"' does (unescaped '#'?)")
            if arg_value is not None:
                raise SyntaxError("Words cannot have an argument, yet '"+
                    name+"' does (unescaped ':'?)")
            if casegen:
                raise SyntaxError("Words cannot generate different cases, yet '"+
                    name+"' does (unescaped '&'?)")
            if randgen is not None or percentage_gen is not None:
                raise SyntaxError("Words cannot have a random generation modifier, yet '"+
                    name+"' does (unescaped '?'?)")
            if parser is not None:
                raise RuntimeError("Internal error: tried to create a word "+
                    "with a pointer to the parser")
            super(WordRuleContent, self).__init__(name, leading_space=leading_space,
                                            variation_name=None, arg_value=None,
                                            casegen=False, randgen=None,
                                            percentage_gen=None, parser=None)
            self.word = name

    def can_have_casegen(self):
        return contains_letters(self.word)


    def generate_random(self, arg_value=None):
        if self.leading_space:
            return {
                "text": ' '+self.word,
                "entities": [],
            }
        return {
            "text": self.word,
            "entities": [],
        }

    def generate_all(self):
        if self.leading_space:
            return [{
                "text": ' '+self.word,
                "entities": [],
            }]
        return [{
            "text": self.word,
            "entities": [],
        }]

    def get_nb_possible_generated_examples(self):
        return 1


class WordGroupRuleContent(RuleContent):
    """
    Represents a word group token inside a rule
    Accepted modifiers:
        - leading-space: bool
        - casegen: bool
        - randgen: str
        - percentgen: bool
    """
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            if variation_name is not None:
                raise SyntaxError("Word groups cannot have variations, yet '"+
                    name+"' does (unescaped '#'?)")
            if arg_value is not None:
                raise SyntaxError("Word groups cannot have an argument, yet '"+
                    name+"' does (unescaped '$'?)")
            if parser is not None:
                raise RuntimeError("Internal error: tried to create a word "+
                    "group with a pointer to the parser")

            if not contains_letters(name):
                casegen = False

            super(WordGroupRuleContent, self).__init__(name,
                                                 leading_space=leading_space,
                                                 variation_name=None,
                                                 arg_value=None,
                                                 casegen=casegen,
                                                 randgen=randgen,
                                                 percentage_gen=percentage_gen,
                                                 parser=None)
            self.words = name

    def can_have_casegen(self):
        return contains_letters(self.words)


    def generate_random(self, generated_randgens=dict()):
        # Manage randgen
        if self.randgen is not None and self.randgen in generated_randgens:
            if generated_randgens[self.randgen]:
                pass  # Must be generated
            else:
                return EMPTY_GEN()  # Cannot be generated
        elif self.randgen is not None:
            if randint(0,99) >= self.percentgen:
                # Don't generated this randgen
                generated_randgens[self.randgen] = False
                return EMPTY_GEN()
            else:
                # Generate this randgen
                generated_randgens[self.randgen] = True

        # Generate the string according to the parameters of the object
        generated_str = self.words
        if self.casegen:
            generated_str = randomly_change_case(generated_str)
        if self.leading_space and may_get_leading_space(generated_str):
            generated_str = ' '+generated_str

        return {
            "text": generated_str,
            "entities": [],
        }

    def generate_all(self):
        generated_examples = []
        if self.randgen is not None:
            generated_examples.append("")

        if self.casegen:
            generated_examples.append(with_leading_lower(self.words))
            generated_examples.append(with_leading_upper(self.words))
        else:
            generated_examples.append(self.words)

        if self.leading_space:
            for (i, ex) in enumerate(generated_examples):
                if may_get_leading_space(ex):
                    generated_examples[i] = ' '+ex

        result = [{"text": ex, "entities": []} for ex in generated_examples]
        return result

    def get_nb_possible_generated_examples(self):
        nb_possible_ex = 1
        if self.casegen:
            nb_possible_ex *= 2
        if self.randgen is not None:
            nb_possible_ex += 1
        return nb_possible_ex
