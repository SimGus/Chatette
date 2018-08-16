#!/usr/bin/env python3

import json

from utils import *


def cast_to_unicode(any):
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
            self.generate_example(intent_name, gen_rule)

        self.write_JSON()

    def generate_example(self, intent_name, rule):
        """Generates an example with a sentence and possibly entities inside it"""
        printDBG("Generating intent: "+intent_name)


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
