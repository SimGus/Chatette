#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO shouldn't generate twice the same statement

import io
import json

from chatette.utils import cast_to_unicode, printDBG


class Generator(object):
    """
    Using the info parsed from the input file, this class will generate
    a Rasa NLU dataset and dump it in a JSON file.
    If there were inconsistencies in the input file, they are likely to be
    detected here.
    """
    DEFAULT_MAX_NB_INTENT_EXAMPLES = 20000

    def __init__(self, parser):
        self.parser = parser
        self.max_nb_single_intent_examples = \
            Generator.DEFAULT_MAX_NB_INTENT_EXAMPLES

    def set_max_nb_single_intent_examples(self, new_max):
        self.max_nb_single_intent_examples = new_max

    def generate_train(self):
        printDBG("Generating training examples...")
        for intent_name in self.parser.intent_definitions:
            intent = self.parser.intent_definitions[intent_name]
            examples = intent.generate(self.max_nb_single_intent_examples)
            for example in examples:
                yield example

    def generate_test(self, training_examples=None):
        should_generate_test_set = False

        for intent_name in self.parser.intent_definitions:
            if self.parser.intent_definitions[intent_name].nb_testing_examples_asked is not None:
                should_generate_test_set = True
                break

        if should_generate_test_set:
            printDBG("Generating testing examples...")
            for intent_name in self.parser.intent_definitions:
                intent = self.parser.intent_definitions[intent_name]
                examples = intent.generate(self.max_nb_single_intent_examples, training_examples)
                for example in examples:
                    yield example

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

    def write_JSON(self, generated_examples, file_path):
        raw_json_data = {
            "rasa_nlu_data": {
                "common_examples": generated_examples,
                "regex_features": [],
                "entity_synonyms":
                    to_Rasa_synonym_format(self.get_entities_synonyms()),
            }
        }
        json_data = cast_to_unicode(raw_json_data)
        with io.open(file_path, 'w', encoding="utf-8") as out_file:
            out_file.write(json.dumps(json_data,
                                      ensure_ascii=False,  # output in utf-8
                                      indent=2,  # More readable
                                      sort_keys=True))  # Deterministic


if __name__ == "__main__":
    import warnings

    warnings.warn("You are running the wrong file ('generator.py')." +
                  "The file that should be run is '__main__.py'.")
