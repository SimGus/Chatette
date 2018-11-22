#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import re
from copy import deepcopy
import sys

try:
   from chatette.parser_utils import Unit, choose
except ImportError:
   from parser_utils import Unit, choose

def EMPTY_GEN():
    return deepcopy({  # NOTE: deepcopy is needed to avoid rewriting on old data
        "text": "",
        "entities": [],
    })


def cast_to_unicode(any):
    if sys.version_info[0] == 3:
        return any
    if isinstance(any, str):
        return unicode(any, "utf-8")
    elif isinstance(any, dict):
        return {cast_to_unicode(key): cast_to_unicode(val)
                for (key, val) in any.iteritems()}  # NOTE: this code works since it is executed only by python 2 (`iteritems` doesn't exist in python 3)
    elif isinstance(any, list):
        return [cast_to_unicode(e) for e in any]
    else:
        return any


def contains_letters(text):
    """Returns `True` if casegen would have an influence on `text`."""
    for c in text:
        if c.isalpha():
            return True
    return False

def randomly_change_case(text):
    """Randomly set the case of the first letter of `text`"""
    if randint(0, 99) >= 50:
        return with_leading_lower(text)
    else:
        return with_leading_upper(text)
def with_leading_upper(text):
    """Returns `text` with a leading uppercase letter"""
    for (i, c) in enumerate(text):
        if not c.isspace():
            return text[:i] + text[i].upper() + text[(i+1):]
    return text
def with_leading_lower(text):
    """Returns `text` with a leading lowercase letter"""
    for (i, c) in enumerate(text):
        if not c.isspace():
            return text[:i] + text[i].lower() + text[(i+1):]
    return text


def may_get_leading_space(text):
    return (text != "" and not text.startswith(' '))


class UnitDefinition(object):
    """Superclass representing a unit definition."""
    def __init__(self, name, rules=[], arg=None, casegen=False):
        self.type = "unit"

        self.name = name
        self.rules = rules  # list of list of `RulesContent`s => [[RulesContent]]

        self.argument_identifier = arg
        if arg is not None:
            pattern_arg = r"(?<!\\)\$"+arg
            self.arg_regex = re.compile(pattern_arg)
        else:
            self.arg_regex = None

        self.variations = dict()

        self.casegen = casegen # IDEA: don't make the casegen variation agnostic

    def can_have_casegen(self):  # TODO: manage variations
        """
        Returns `True` if casegen may have an influence on
        any of the rules of this definition.
        """
        for rule in self.rules:
            if len(rule) > 0 and rule[0].can_have_casegen():
                    return True
        return False


    def add_rule(self, rule, variation_name=None, slot_val=None):
        # (RuleContent, str, str) -> ()
        rule.set_slot_value
        if variation_name is None:
            self.rules.append(rule)
        else:
            if variation_name == "":
                raise SyntaxError("Defining a "+self.type+" with an empty name"+
                    "is not allowed")
            if variation_name not in self.variations:
                self.variations[variation_name] = [rule]
            else:
                self.variations[variation_name].append(rule)
            self.rules.append(rule)
    def add_rules(self, rules, variation_name=None, slot_val=None):
        # ([RuleContent], str, str) -> ()
        self.rules.extend(rules)
        if variation_name is not None:
            if variation_name == "":
                raise SyntaxError("Defining a "+self.type+" with an empty name"+
                    "is not allowed")
            if variation_name not in self.variations:
                self.variations[variation_name] = rules
            else:
                self.variations[variation_name].extend(rules)

    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of your rule at random and
        returns the string generated and the entities inside it as a dict.
        """
        # (str, str) -> {"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}
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

        generated_example = EMPTY_GEN()
        generated_randgens = dict()
        for token in chosen_rule:
            generated_token = token.generate_random(generated_randgens)
            generated_example["text"] += generated_token["text"]
            generated_example["entities"].extend(generated_token["entities"])

        if self.casegen:
            generated_example["text"] = randomly_change_case(generated_example["text"])

        # Replace `arg` inside the generated sentence
        if arg_value is not None and self.argument_identifier is not None:
            generated_example["text"] = \
                self.arg_regex.sub(arg_value, generated_example["text"])
            generated_example["text"] = \
                generated_example["text"].replace("\$", "$")

        return generated_example

    def generate_all(self, variation_name=None, arg_value=None):
        generated_examples = []

        relevant_rules = self.rules
        if variation_name is not None:
            if variation_name in self.variations:
                relevant_rules = self.variations[variation_name]
            else:
                raise SyntaxError("Couldn't find variation '"+
                                  str(variation_name)+"' for "+str(self.type)+
                                  " '"+str(self.name)+"'")

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
            generated_examples.extend(examples_from_current_rule)

        # Replace `arg` inside generated sentences
        if arg_value is not None and self.argument_identifier is not None:
            for (i, ex) in enumerate(generated_examples):
                ex["text"] = self.arg_regex.sub(arg_value, ex["text"])
                generated_examples[i]["text"] = ex["text"].replace("\$", "$")
        return generated_examples

    def get_nb_possible_generated_examples(self, variation_name=None):
        """Returns the number of examples that can be generated by this token."""
        relevant_rules = self.rules
        if variation_name is not None:
            if variation_name in self.variations:
                relevant_rules = self.variations[variation_name]
            else:
                raise SyntaxError("Couldn't find variation '"+variation_name+
                    "' for "+self.type+" '"+self.name+"'")

        nb_possible_ex = 0
        for rule in relevant_rules:
            rule_nb_ex = 0
            for sub_unit_rule in rule:
                current_nb_ex = sub_unit_rule.get_nb_possible_generated_examples()
                if current_nb_ex is None:
                    continue
                if rule_nb_ex == 0:
                    rule_nb_ex = current_nb_ex
                else:
                    rule_nb_ex *= current_nb_ex
            nb_possible_ex += rule_nb_ex

        if self.casegen:
            nb_possible_ex *= 2
        return nb_possible_ex


    def printDBG(self):
        print("\t"+self.type+": "+self.name)
        print("\t\targument: "+str(self.argument_identifier))
        print("\t\tcasegen: "+str(self.casegen))
        print("\t\trules:")
        for rule in self.rules:
            print("\t\t\trule:")
            for content in rule:
                content.printDBG(4)
        for variation in self.variations:
            print("\t\tvariation "+variation)
            for rule in self.variations[variation]:
                print("\t\t\trule:")
                for content in rule:
                    content.printDBG(3)
        print("")


class RuleContent(object):
    """
    Superclass represents anything that can be inside a rule:
    for words and word groups, it generates as is;
    for units, it is a link to a definition that can be generated.
    The rule also contains modifier used during the generation, such as:
        - leading-space: bool (a leading space will be added to the generated str)
        - casegen: bool (the first letter may be in upper- or lowercase)
        - randgen: str (if not `None` it might not be generated,
                        and if it is the same string than for another rule,
                        it will generate iff the other rule generated (and vice-versa))
        - percentgen: int (if `randgen` is enable, this is the percentage of
                           of chances that this rule will generate something)
        - arg: str (represents the identifier of an argument inside the rule,
                    which will be replaced by a value given upon generation)
        - variation-name: str (identifies which variation of the definition
                               we are calling)
    """
    def __init__(self, name, leading_space=False, variation_name=None,
        arg_value=None, casegen=False, randgen=None, percentage_gen=50,
        parser=None):
            if name is None or name == "":
                raise SyntaxError("Tried to create content without a contents (or a name)")
            self.name = name
            self.variation_name = variation_name
            self.arg_value = arg_value

            self.leading_space = leading_space

            self.casegen = casegen
            self.randgen = randgen
            if percentage_gen is not None:
                self.percentgen = int(percentage_gen)
            else:
                self.percentgen = 50

            self.parser = parser

    def can_have_casegen(self):
        """Returns `True` if casegen can have an influence on this rule."""
        return False


    def generate_random(self, generated_randgens={}):
        """
        Returns a string and its entities randomly generated from the rules the
        object represents. May return an empty string if `randgen` is enabled.
        `generated_randgens` is a dict of all the randgen names that have been
        decided as to generate or not, i.e. if "some randgen" is in
        `generated_randgens` and its value is `True`, all contents with this
        randgen must be generated; if its value is `False`, it cannot be
        generated; otherwise you can choose and put it into `generated_randgens`.
        """
        return EMPTY_GEN()

    def generate_all(self):
        """
        Returns a list of all the strings and entities that can be generated
        from the rules this object represents. May include the empty string if
        it can be generated.
        """
        return [EMPTY_GEN()]

    def get_nb_possible_generated_examples(self):
        """Returns the number of examples that can be generated by this token."""
        pass


    def printDBG(self, nb_indent=0):
        # (int) -> ()
        indentation = nb_indent*'\t'
        print(indentation+self.name)
        print(indentation+"\tvariation name: "+str(self.variation_name))
        print(indentation+"\targ value: "+str(self.arg_value))
        print(indentation+"\tcasegen: "+str(self.casegen))
        print(indentation+"\trandgen: "+str(self.randgen)+" with percentage: "
            +str(self.percentgen))
