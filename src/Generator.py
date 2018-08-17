#!/usr/bin/env python3

# TODO shouldn't generate twice the same statement

import sys
import json
from random import randint

from utils import *
from parser_utils import Unit
from rasa_adapter import to_Rasa_format

EMPTY_GEN = {
    "text": '',
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
        self.generated_randgens = dict()

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
        max_gen_nb = None
        if "nb-gen-asked" not in intent_rules:  # Different flavors (variations)
            for variation in intent_rules:
                self.generate_intent(intent_name, intent_rules[variation])
        else:
            max_gen_nb = intent_rules["nb-gen-asked"]

        if max_gen_nb is not None:
            max_gen_nb = int(max_gen_nb)
            nb_examples_gen = 0
            nb_intent_rules = len(intent_rules["rules"])

            while nb_examples_gen < max_gen_nb:
                current_example = ""
                current_entities = []
                # Choose rule to generate
                rule_index = randint(0, nb_intent_rules-1)
                intent_rule = intent_rules["rules"][rule_index]
                # Generate each unit in the rule
                for unit_rule in intent_rule:
                    self.generated_randgens = dict()
                    generation = self.generate_unit(unit_rule)
                    current_example += generation["text"]
                    current_entities.extend(generation["entities"])
                current_example = current_example.lstrip()
                printDBG("Generated: '"+current_example+"'")
                printDBG("Entities: "+str(current_entities))
                self.generated_examples.append(
                    to_Rasa_format(intent_name, current_example, current_entities)
                )
                nb_examples_gen += 1
        else:  #TODO
            print("Generation without max number is currently not supported")

    def generate_unit(self, unit_rule):
        """
        Generates a unit from its rule and returns
        a dict with the generated string (potentially with a leading space)
        and potentially info about generated entities
        (their slot name, value and text into a list of dicts).
        The string can be empty if the generation can randomly not be done.
        The return value indexes are 'text' and 'entities'.
        'entities' will be an empty list if no enitity was generated.
        'generated_randgens' is a dict with keys the name of the randgen and
        a boolean if they were generated or not before.
        """
        unit_type = unit_rule["type"]
        if unit_type == Unit.word:
            if unit_rule["leading-space"]:
                return {
                    "text": ' '+unit_rule["word"],
                    "entities": [],
                }
            return {
                "text": unit_rule["word"],
                "entities": [],
            }
        elif unit_type == Unit.choice:  # TODO casegen
            if unit_rule["randgen"]:
                if randint(0, 99) >= 50:
                    return EMPTY_GEN

            chosen_index = randint(0, len(unit_rule["choices"])-1)
            chosen_rule = unit_rule["choices"][chosen_index]
            generated_str = ""
            generated_entities = []
            # Generate each unit of the rule
            for sub_unit_rule in chosen_rule:
                sub_generation = self.generate_unit(sub_unit_rule)
                generated_entities.extend(sub_generation["entities"])
                generated_str += sub_generation["text"]
            # Add a space at the front if needed
            if generated_str != "" and unit_rule["leading-space"] and \
                not generated_str.startswith(' '):
                    generated_str = ' '+generated_str

            return {
                "text": generated_str,
                "entities": generated_entities,
            }
        else:
            # TODO keep track of already generated sentences (+max nb of attempts)
            # Manage random generation
            randgen_name = unit_rule["randgen"]
            if randgen_name is not None:
                if randgen_name not in self.generated_randgens:  # not yet tested
                    percentage_gen = 50
                    if unit_rule["percentgen"] is not None:  # TODO seems to be a problem with this
                        percentage_gen = int(unit_rule["percentgen"])
                    if randint(0, 99) >= percentage_gen:
                        if randgen_name != "":
                            self.generated_randgens[randgen_name] = False  # TODO do it by level
                        return EMPTY_GEN
                    elif randgen_name != "":
                        self.generated_randgens[randgen_name] = True
                elif not self.generated_randgens[randgen_name]:  # Should not be generated
                    return EMPTY_GEN
                else:  # Must be generated
                    pass

            generate_different_case = False
            if "casegen" in unit_rule and unit_rule["casegen"]:
                generate_different_case = True

            generated_str = ""
            generated_entities = []
            unit_def = None
            if unit_type == Unit.word_group:
                if unit_rule["leading-space"]:
                    generated_str += ' '
                generated_str += unit_rule["words"]

                if generate_different_case:
                    return {
                        "text": randomly_change_case(generated_str),
                        "entities": [],
                    }
                return {
                    "text": generated_str,
                    "entities": [],
                }

            elif unit_type == Unit.alias or unit_type == Unit.slot:
                unit_def = None
                if unit_type == Unit.alias:
                    if unit_rule["name"] not in self.parser.aliases:
                        raise SyntaxError("Alias '"+unit_rule["name"]+"' wasn't defined")
                    unit_def = self.parser.aliases[unit_rule["name"]]
                else:
                    if unit_rule["name"] not in self.parser.slots:
                        raise SyntaxError("Slot '"+unit_rule["name"]+"' wasn't defined")
                    unit_def = self.parser.slots[unit_rule["name"]]

                # Manage variations
                variation = unit_rule["variation"]
                if variation is not None:
                    if isinstance(unit_def, dict) and variation in unit_def:
                        unit_def = unit_def[variation]
                    elif unit_type == Unit.alias:
                        raise SyntaxError(
                            "Couldn't find variation '" + unit_rule["variation"] +
                            "' for alias named '" + unit_rule["name"] + "'"
                        )
                    else:
                        raise SyntaxError(
                            "Couldn't find variation '" + unit_rule["variation"] +
                            "' for slot named '" + unit_rule["name"] + "'"
                        )
                elif isinstance(unit_def, dict):  # No variation asked but the unit is defined with variations
                    unit_def = unit_def["all-variations-aggregation"]

                # Choose rule
                rule_index = randint(0, len(unit_def)-1)
                chosen_rule = unit_def[rule_index]
                alt_slot_val_name = None
                if isinstance(chosen_rule, dict):
                    alt_slot_val_name = chosen_rule["slot-value-name"]
                    chosen_rule = chosen_rule["rule"]
                # Generate each unit of the rule
                for sub_unit_rule in chosen_rule:
                    sub_generation = self.generate_unit(sub_unit_rule)
                    generated_entities.extend(sub_generation["entities"])
                    generated_str += sub_generation["text"]

                # Manage entities
                if unit_type == Unit.slot:
                    if alt_slot_val_name == '/':
                        alt_slot_val_name = generated_str
                    generated_entities.extend([{
                        "slot-name": unit_rule["name"],
                        "text": generated_str,
                        "value": alt_slot_val_name,
                    }])

            elif unit_type == Unit.intent:
                if unit_rule["name"] not in self.parser.intents:
                    raise SyntaxError("Intent '"+unit_rule["name"]+"' wasn't defined")
                unit_def = self.parser.intents[unit_rule["name"]]

                # Manage variations
                variation = unit_rule["variation"]
                if variation is not None:
                    if "nb-gen-asked" not in unit_def:
                            unit_def = unit_def[variation]["rules"]
                    else:
                        raise SyntaxError(
                            "Couldn't find variation '" + unit_rule["variation"] +
                            "' for intent named '" + unit_rule["name"] + "'"
                        )
                elif "rules" in unit_def:
                    unit_def = unit_def["rules"]
                else:  # No variation asked but the unit is defined with variations
                    unit_def = unit_def["all-variations-aggregation"]["rules"]

                # Choose rule
                rule_index = randint(0, len(unit_def)-1)
                chosen_rule = unit_def[rule_index]
                # Generate each unit of the rule
                for sub_unit_rule in chosen_rule:
                    sub_generation = self.generate_unit(sub_unit_rule)
                    generated_entities.extend(sub_generation["entities"])
                    generated_str += sub_generation["text"]

            else:
                raise RuntimeError("Tried to generate a unit of unknown type")

            if generated_str != "" and unit_rule["leading-space"] and \
                not generated_str.startswith(' '):
                    generated_str = ' '+generated_str

            if generate_different_case:
                return {
                    "text": randomly_change_case(generated_str),
                    "entities": generated_entities,
                }
            return {
                "text": generated_str,
                "entities": generated_entities,
            }


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
