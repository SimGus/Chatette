#!/usr/bin/env python3

# TODO shouldn't generate twice the same statement

import json

from utils import *
from parser_utils import Unit
from rasa_adapter import to_Rasa_format


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
