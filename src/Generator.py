#!/usr/bin/env python3

# TODO shouldn't generate twice the same statement

import json

from utils import *
from parser_utils import Unit
from rasa_adapter import *


class Generator(object):
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
        for intent_name in self.parser.intent_definitions:
            current_examples = self.parser.intent_definitions[intent_name].generate()
            formatted_examples = []
            for ex in current_examples:
                formatted_examples.append(to_Rasa_format(intent_name, ex))
            self.generated_examples.extend(formatted_examples)

        printDBG("Generation over, writing to file...")
        self.write_JSON()


    def get_entities_synonyms(self):
        """
        Makes a dict of all the synonyms of entities
        based on the slot value they are assigned.
        """
        synonyms = dict()
        for slot_definition in self.parser.slot_definitions:
            current_synonyms_dict = \
                self.parser.slot_definitions[slot_definition].get_synonyms_dict()
            for slot_value in current_synonyms_dict:
                if slot_value not in synonyms:
                    synonyms[slot_value] = current_synonyms_dict[slot_value]
                else:
                    synonyms[slot_value].extend(current_synonyms_dict[slot_value])
        return synonyms

    def generate_all_possibilities(self, unit_rule, arg=None):
        """
        Generates all the possible values that the rule 'unit_rule' can generate
        (including the empty generation if possible) and returns them all
        as a list of dict.
        """
        # {} or [] -> [{"text": str, "entities": [...]}]
        if isinstance(unit_rule, list):
            generated_texts = []
            examples_from_sub_rules = []
            tmp_buffer = []
            for sub_unit_rule in unit_rule:
                sub_unit_possibilities = \
                    self.generate_all_possibilities(sub_unit_rule, arg)
                tmp_buffer = []
                if len(examples_from_sub_rules) == 0:
                    examples_from_sub_rules = sub_unit_possibilities
                else:
                    for ex in examples_from_sub_rules:
                        for possibility in sub_unit_possibilities:
                            tmp_buffer.append({
                                "text": ex["text"]+possibility["text"],
                                "entities": ex["entities"]+possibility["entities"]
                            })
                    examples_from_sub_rules = tmp_buffer
            generated_texts.extend(examples_from_sub_rules)
            return generated_texts

        if "type" not in unit_rule:
            return self.generate_all_possibilities(unit_rule["rule"], arg)

        unit_type = unit_rule["type"]
        if unit_type == Unit.word:
            if unit_rule["leading-space"]:
                return [{
                    "text": ' '+unit_rule["word"],
                    "entities": [],
                }]
            return [{
                "text": unit_rule["word"],
                "entities": [],
            }]
        elif unit_type == Unit.word_group:
            # TODO manage `arg`
            generated_texts = []
            if unit_rule["randgen"] is not None:
                generated_texts.append(EMPTY_GEN)

            generated_str = ""
            if unit_rule["leading-space"]:
                generated_str += ' '
            generated_str += unit_rule["words"]

            if "casegen" in unit_rule and unit_rule["casegen"]:
                generated_texts.append({
                    "text": with_leading_lower(generated_str),
                    "entities": [],
                })
                generated_texts.append({
                    "text": with_leading_upper(generated_str),
                    "entities": [],
                })
            else:
                generated_texts.append({
                    "text": generated_str,
                    "entities": [],
                })
            return generated_texts
        elif unit_type == Unit.choice:
            generated_texts = []
            if unit_rule["randgen"] is not None:
                generated_texts.append(EMPTY_GEN)

            for choice in unit_rule["choices"]:
                examples_from_sub_rules = []
                tmp_buffer = []
                for sub_unit_rule in choice:
                    sub_unit_possibilities = \
                        self.generate_all_possibilities(sub_unit_rule, arg)
                    tmp_buffer = []
                    if len(examples_from_sub_rules) == 0:
                        examples_from_sub_rules = sub_unit_possibilities
                    else:
                        for ex in examples_from_sub_rules:
                            for possibility in sub_unit_possibilities:
                                tmp_buffer.append({
                                    "text": ex["text"]+possibility["text"],
                                    "entities": ex["entities"]+possibility["entities"]
                                })
                        examples_from_sub_rules = tmp_buffer
                generated_texts.extend(examples_from_sub_rules)

            if unit_rule["leading-space"]:
                for ex in generated_texts:
                    text = ex["text"]
                    if text != "" and not text.startswith(' '):
                        ex["text"] = ' '+text

            return generated_texts
        else:
            generated_texts = []
            if unit_rule["randgen"] is not None:
                generated_texts.append(EMPTY_GEN)

            current_arg_name = None

            if unit_type == Unit.alias or unit_typ == Unit.slot:
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
                    if variation in unit_def:
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
                elif "rules" not in unit_def:  # No variation asked but the unit is defined with variations
                    unit_def = unit_def["all-variations-aggregation"]  # TODO check this with arg

                # Get arg identifier
                if isinstance(unit_def, dict):
                    current_arg_name = unit_def["arg"]
                    if current_arg_name is not None:
                        print("arg: "+str(current_arg_name))
                    if current_arg_name == "":
                        current_arg_name = None

                    unit_def = unit_def["rules"]

                if len(unit_def) > 0:
                    for rule in unit_def:
                        if isinstance(rule, dict):
                            rule = rule["rule"]

                        examples_from_sub_rules = []
                        tmp_buffer = []
                        for sub_unit_rule in rule:
                            sub_unit_possibilities = \
                                self.generate_all_possibilities(sub_unit_rule, arg)
                            tmp_buffer = []
                            if len(examples_from_sub_rules) == 0:
                                examples_from_sub_rules = sub_unit_possibilities
                            else:
                                for ex in examples_from_sub_rules:
                                    for possibility in sub_unit_possibilities:
                                        tmp_buffer.append({
                                            "text": ex["text"]+possibility["text"],
                                            "entities": ex["entities"]+possibility["entities"]
                                        })
                                examples_from_sub_rules = tmp_buffer
                        generated_texts.extend(examples_from_sub_rules)
                else:  # TODO this should be an error
                    pass
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
                    # Get arg identifier
                    current_arg_name = unit_def["arg"]
                    if current_arg_name is not None:
                        print("arg: "+str(current_arg_name))
                    if current_arg_name == "":
                        current_arg_name = None

                    unit_def = unit_def["rules"]
                else:  # No variation asked but the unit is defined with variations
                    unit_def = unit_def["all-variations-aggregation"]["rules"]

                for rule in unit_def:
                    examples_from_sub_rules = []
                    tmp_buffer = []
                    for sub_unit_rule in rule:
                        sub_unit_possibilities = \
                            self.generate_all_possibilities(sub_unit_rule, arg)
                        tmp_buffer = []
                        if len(examples_from_sub_rules) == 0:
                            examples_from_sub_rules = sub_unit_possibilities
                        else:
                            for ex in examples_from_sub_rules:
                                for possibility in sub_unit_possibilities:
                                    tmp_buffer.append({
                                        "text": ex["text"]+possibility["text"],
                                        "entities": ex["entities"]+possibility["entities"]
                                    })
                            examples_from_sub_rules = tmp_buffer
                    generated_texts.extend(examples_from_sub_rules)
            else:
                raise RuntimeError("Tried to generate a unit of unknown type")

            if unit_rule["leading-space"]:
                for ex in generated_texts:
                    text = ex["text"]
                    if text != "" and not text.startswith(' '):
                        ex["text"] = ' '+text

            if "casegen" in unit_rule and unit_rule["casegen"]:
                casegen_examples = []
                for ex in generated_texts:
                    casegen_examples.append({
                        "text": with_leading_lower(ex["text"]),
                        "entities": ex["entities"],
                    })
                    casegen_examples.append({
                        "text": with_leading_upper(ex["text"]),
                        "entities": ex["entities"],
                    })
                generated_texts = casegen_examples

            # Deal with arguments
            if arg is not None and current_arg_name is not None:
                for (i, ex) in enumerate(generated_texts):
                    pattern_arg = r"(?<!\\)\$"+current_arg_name
                    ex = re.sub(pattern_arg, unit_rule["arg"], ex)
                    generated_texts[i]["text"] = ex.replace("\$", "$")

            return generated_texts


    def get_slots_synonyms(self):
        synonyms = dict()
        for slot_name in self.parser.slots:
            if "rules" in self.parser.slots[slot_name]:  # No variations
                current_arg_val = self.parser.slots[slot_name]["arg"]
                for rule in self.parser.slots[slot_name]["rules"]:
                    current_val = rule["slot-value-name"]
                    rule = rule["rule"]
                    current_all_possibilities = \
                        self.generate_all_possibilities(rule, current_arg_val)
                    if current_val not in synonyms:
                        synonyms[current_val] = []
                    for possibility in current_all_possibilities:
                        text = possibility["text"]
                        if text not in synonyms[current_val]:
                            synonyms[current_val].append(possibility["text"].strip())
            else:  # Variations
                for variation in self.parser.slots[slot_name]:
                    if "rules" in self.parser.slots[slot_name][variation]:
                        current_arg_val = self.parser.slots[slot_name][variation]["arg"]
                        for rule in self.parser.slots[slot_name][variation]["rules"]:
                            current_val = rule["slot-value-name"]
                            rule = rule["rule"]
                            current_all_possibilities = \
                                self.generate_all_possibilities(rule, current_arg_val)
                            if current_val not in synonyms:
                                synonyms[current_val] = []
                            for possibility in current_all_possibilities:
                                text = possibility["text"]
                                if text not in synonyms[current_val]:
                                    synonyms[current_val].append(possibility["text"].strip())
                    else:  # aggregation of all variations
                        pass
        return synonyms


    def write_JSON(self):
        raw_json_data = {
            "rasa_nlu_data": {
                "common_examples": self.generated_examples,
                "regex_features" : [],
                "entity_synonyms":
                    to_Rasa_synonym_format(self.get_entities_synonyms()),
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
