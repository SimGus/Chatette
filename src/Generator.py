#!/usr/bin/env python3

# TODO shouldn't generate twice the same statement

import sys
import json
from random import randint

from utils import *
from parser_utils import Unit


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
        return text
    for (i, c) in enumerate(text):
        if not c.isspace():
            return text[:i] + text[i].upper() + text[(i+1):]


class Generator():
    """
    Using the info parsed from the input file, this class will generate
    a Rasa NLU dataset and dump it in a JSON file.
    If there were inconsistencies in the input file, they are likely to be
    detected here.
    """
    def __init__(self, output_file, parser):
        self.out_file = output_file
        self.parser = parser
        self.generated_examples = []

    def generate(self):
        print("")
        printDBG("Start generation")
        for intent_name in self.parser.intents:
            gen_rule = self.parser.intents[intent_name]
            self.generate_intent(intent_name, gen_rule)

        self.write_JSON()

    def generate_intent(self, intent_name, intent_rules):
        """
        Generates the asked number of examples for this intent
        given a list of rules.
        """
        printDBG("Generating intent: "+intent_name)
        if isinstance(intent_rules, list):  # Different flavors (variations)
            pass  # TODO
        else:
            if intent_rules["nb-gen-asked"] is not None:
                max_gen_nb = int(intent_rules["nb-gen-asked"])
                nb_examples_gen = 0
                nb_intent_rules = len(intent_rules["rules"])

                while nb_examples_gen < max_gen_nb:
                    current_example = ""
                    # Choose rule to generate
                    rule_index = randint(0, nb_intent_rules-1)
                    intent_rule = intent_rules["rules"][rule_index]
                    # Generate each unit in the rule
                    for unit_rule in intent_rule:
                        current_example += self.generate_unit(unit_rule).replace("  ", ' ')  # TODO it would be better to not have bad spaces in generations
                    printDBG("Generated: "+current_example)
                    self.generated_examples.append(current_example)
                    nb_examples_gen += 1
            else:  #TODO
                print("No nb gen asked not yet supported")

    def generate_unit(self, unit_rule):
        """
        Generates a unit from its rule
        and returns the generated string (potentially with a leading space).
        Returns an empty string if the generation can randomly not be done.
        """
        unit_type = unit_rule["type"]
        if unit_type == Unit.word:
            return ' '+unit_rule["word"]
        else:
            # TODO keep track of already generated sentences (+max nb of attempts)
            # Manage random generation
            if unit_rule["randgen"] is not None:
                percentage_gen = 50
                if unit_rule["percentgen"] is not None:
                    percentage_gen = int(unit_rule["percentgen"])
                if randint(0, 99) >= percentage_gen:
                    return ''

            generate_different_case = False
            if "casegen" in unit_rule and unit_rule["casegen"]:
                generate_different_case = True

            generated_str = ''
            unit_def = None
            if unit_type == Unit.word_group:
                # print("WORD GROUP: "+str(unit_rule))
                if unit_rule["leading-space"]:
                    generated_str += ' '
                generated_str += unit_rule["words"]

                if generate_different_case:
                    return randomly_change_case(generated_str)
                return generated_str
            elif unit_type == Unit.alias:
                if unit_rule["name"] not in self.parser.aliases:
                    raise SyntaxError("Alias '"+unit_rule["name"]+"' wasn't defined")
                unit_def = self.parser.aliases[unit_rule["name"]]
            elif unit_type == Unit.slot:
                if unit_rule["name"] not in self.parser.slots:
                    raise SyntaxError("Alias '"+unit_rule["name"]+"' wasn't defined")
                unit_def = self.parser.slots[unit_rule["name"]]
            elif unit_type == Unit.intent:
                if unit_rule["name"] not in self.parser.intents:
                    raise SyntaxError("Alias '"+unit_rule["name"]+"' wasn't defined")
                unit_def = self.parser.intents[unit_rule["name"]]
            else:
                raise RuntimeError("Tried to generate a unit of unknown type")

            if isinstance(unit_def, list):  # TODO tmp variation not supported
                unit_def = unit_def[0]

            if unit_rule["leading-space"]:
                generated_str += ' '

            # Choose rule
            rule_index = randint(0, len(unit_def["rules"])-1)
            chosen_rule = unit_def["rules"][rule_index]
            if isinstance(chosen_rule, dict):
                chosen_rule = chosen_rule["rule"]
            # Generate each unit of the rule
            for sub_unit_rule in chosen_rule:
                generated_str += self.generate_unit(sub_unit_rule)

            if generate_different_case:
                return randomly_change_case(generated_str)
            return generated_str


    def write_JSON(self):
        raw_json_data = {
            "rasa_nlu_data": {
                "common_examples": self.generated_examples,
                "regex_features" : [],
                "entity_synonyms": []
            }
        }
        json_data = cast_to_unicode(raw_json_data)
        self.out_file.write(
            json.dumps(json_data, ensure_ascii=False, indent=2, sort_keys=True)
        )


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('Generator.py')." +
        "The file that should be run is 'main.py'.")
