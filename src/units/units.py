#!/usr/bin/env python3

from random import randint
import re

from parser_utils import Unit

EMPTY_GEN = {
    "text": "",
    "entities": [],
}


def cast_to_unicode(any):
    if sys.version_info[0] == 3:
        return any
    if isinstance(any, str):
        return unicode(any, "utf-8")
    elif isinstance(any, dict):
        cast_dict = dict()
        for key in any:
            cast_key = cast_to_unicode(key)
            cast_value = cast_to_unicode(any[key])
            cast_dict[cast_key] = cast_value
        return cast_dict
    elif isinstance(any, list):
        cast_list = []
        for e in any:
            cast_list.append(cast_to_unicode(e))
        return cast_list
    else:
        return any


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
            return text[:i] + text[i].upper() + text[(i+1):]
    return text


def may_get_leading_space(text):
    return (text != "" and not text.startswith(' '))


class UnitDefinition():
    """Superclass representing a unit definition."""
    def __init__(self, name, rules=[], arg=None, casegen=False):
        self.type = "unit"

        self.name = name
        self.rules = rules

        self.argument_identifier = arg
        pattern_arg = r"(?<!\\)\$"+arg
        self.arg_regex = re.compile(pattern_arg)

        self.variations = dict()

        self.casegen = casegen


    def add_rule(self, rule, variation_name=None):
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

    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of your rule at random and
        returns the string generated and the entities inside it as a dict.
        """
        # (str, str) -> {"text": str, "entities": [str]}
        chosen_rule = None
        if variation_name is None:
            chosen_rule = self.rules[randint(0,len(self.rules)-1)]
        else:
            if variation_name not in self.variations:
                raise SyntaxError("Couldn't find a variation named '"+
                    variation_name+"' for "+self.type+" '"+self.name+"'")
            max_index = len(self.variations[variation_name])-1)
            chosen_rule = \
                self.variations[variation_name][randint(0, max_index)]

            generated_example = EMPTY_GEN
            for token in chosen_rule:
                generated_token = token.generate_random()
                generated_example["text"] += generated_token["text"]
                generated_example["entities"].extend(generated_token["entities"])

        if self.casegen:
            generated_example["text"] = randomly_change_case(generated_example["text"])

        # Replace `arg` inside the generated sentence
        if arg_value is not None and self.argument_identifier is not None:
            generated_example["text"] = \
                self.arg_regex.sub(arg_value, generated_example["text"])
            generated_example[text] = \
                generated_example["text"].replace("\$", "$")

        return generated_example

    def generate_all(self, arg_value=None):  # TODO should i manage variations in here?
        generated_examples = []

        for rule in self.rules:
            examples_from_sub_rules = []
            tmp_buffer = []
            for sub_unit_rule in rule:
                sub_unit_possibilities = \
                    sub_unit_rule.generate_all()
                if len(examples_from_sub_rules) == 0:
                    examples_from_sub_rules = sub_unit_possibilities
                else:
                    tmp_buffer = []
                    for ex in examples_from_sub_rules:
                        for possibility in sub_unit_possibilities:
                            tmp_buffer.append({
                                "text": ex["text"]+possibility["text"],
                                "entities": ex["entities"]+possibility["entities"]
                            })
                    examples_from_sub_rules = tmp_buffer
            generated_examples.extend(examples_from_sub_rules)

        # Replace `arg` inside generated sentences
        if arg_value is not None and self.argument_identifier is not None:
            for (i, ex) in enumerate(generated_examples):
                ex["text"] = self.arg_regex.sub(arg_value, ex["text"])
                generated_examples[i]["text"] = ex["text"].replace("\$", "$")
        return generated_examples


class Rule():
    """
    Represents anything that can be inside a rule:
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
    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None,
        casegen=False, randgen=None, percentage_gen=50, parser=None):
            self.name = name
            self.variation_name = variation_name
            self.arg_value = arg_value

            self.casegen = casegen
            self.randgen = randgen
            self.percentgen = percentage_gen

            self.parser = parser

    def generate_random(self):
        """
        Returns a string and its entities randomly generated from the rules the
        object represents. May return an empty string if `randgen` is enabled.
        """
        # () -> {"text": str, "entities": [str]}
        pass

    def generate_all(self):
        """
        Returns a list of all the strings and entities that can be generated
        from the rules this object represents. May include the empty string if
        it can be generated.
        """
        # () -> [{"text": str, "entities": [str]}]
        pass
