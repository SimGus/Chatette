# coding: utf-8
"""
Module `chatette.adapters.rasa`
Contains the definition of the adapter that writes output in JSON
for Rasa NLU.
"""

import io
import json

from chatette.utils import cast_to_unicode
from ._base import Adapter


class RasaAdapter(Adapter):
    def __init__(self, base_filepath=None, batch_size=10000):# -> None:
        super(RasaAdapter, self).__init__(base_filepath, batch_size)
        self._base_file_contents = None

    @classmethod
    def _get_file_extension(cls):
        return "json"


    def _write_batch(self, output_file_handle, batch):
        rasa_entities = [self.prepare_example(ex) for ex in batch.examples]  # TODO rename this?

        json_data = self._get_base_to_extend()
        json_data["rasa_nlu_data"]["common_examples"] = rasa_entities
        json_data["rasa_nlu_data"]["entity_synonyms"] = \
            self.__format_synonyms(batch.synonyms)
        json_data = cast_to_unicode(json_data)

        output_file_handle.write(
            json.dumps(json_data, ensure_ascii=False, indent=2, sort_keys=True)
        )


    def prepare_example(self, example):
        def entity_to_rasa(entity):
            return {
                "entity": entity.slot_name,
                "value": entity.value,
                "start": entity._start_index,
                "end": entity._start_index + entity._len,
            }

        return {
            "intent": example.intent_name,
            "text": example.text,
            "entities": [entity_to_rasa(entity) for entity in example.entities]
        }

    @classmethod
    def __format_synonyms(cls, synonyms):
        # {str: [str]} -> [{"value": str, "synonyms": [str]}]
        return [
            {
                "value": slot_name,
                "synonyms": synonyms[slot_name]
            }
            for slot_name in synonyms
            if len(synonyms[slot_name]) > 1
        ]


    def _get_base_to_extend(self):
        if self._base_file_contents is None:
            if self._base_filepath is None:
                return self._get_empty_base()
            with io.open(self._base_filepath, 'r') as base_file:
                self._base_file_contents = json.load(base_file)
            self.check_base_file_contents()
        return self._base_file_contents

    def _get_empty_base(self):
        return {
            "rasa_nlu_data": {
                "common_examples": None,
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": None,
            }
        }

    def check_base_file_contents(self): 
        """
        Checks that `self._base_file_contents` contains well formatted JSON.
        Throws a `SyntaxError` if the data is incorrect.
        """
        if self._base_file_contents is None:
            return
        if not isinstance(self._base_file_contents, dict):
            self._base_file_contents = None
            raise SyntaxError(
                "Couldn't load valid data from base file '" + \
                self._base_filepath + "'"
            )
        else:
            if "rasa_nlu_data" not in self._base_file_contents:
                self._base_file_contents = None
                raise SyntaxError(
                    "Expected 'rasa_nlu_data' as a root of base file '" + \
                    self._base_filepath + "'")
