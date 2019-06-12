import json

from chatette.units import ENTITY_MARKER
from chatette.utils import cast_to_unicode
from ._base import Adapter


class RasaAdapter(Adapter):
    def __init__(self, base_filepath=None, batch_size=10000):# -> None:
        super(RasaAdapter, self).__init__(base_filepath, batch_size)
        self._base_file_contents = None

    def _get_file_extension(self):
        return "json"


    def prepare_example(self, example):
        def entity_to_rasa(entity):
            first_index = self.__find_entity(example.text, entity["text"])
            entity["text"] = entity["text"].rstrip()
            # NOTE: This always finds something
            # Remove the entity marker of this entity
            # (works unless entities are not recorded in order)
            example.text = example.text[:first_index] + \
                            example.text[first_index+len(ENTITY_MARKER):]
            return {
                "value": entity["value"],
                "entity": entity["slot-name"],
                "start": first_index,
                "end": first_index + len(entity["text"]),
            }

        return {
            "intent": example.name,
            "entities": [entity_to_rasa(e) for e in example.entities],
            # HACK: Call `entity_to_rasa` BEFORE storing "text" here
            #       (this function removes the entity markers)
            "text": example.text,
        }


    def _write_batch(self, output_file_handle, batch):
        rasa_entities = [self.prepare_example(ex) for ex in batch.examples]

        json_data = self._get_base_to_extend()
        json_data["rasa_nlu_data"]["common_examples"] = rasa_entities
        json_data["rasa_nlu_data"]["entity_synonyms"] = \
            self.__synonym_format(batch.synonyms)
        json_data = cast_to_unicode(json_data)

        output_file_handle.write(json.dumps(json_data, ensure_ascii=False,
                                            indent=2, sort_keys=True))

    @classmethod
    def __synonym_format(cls, synonyms):
        # {str: [str]} -> [{"value": str, "synonyms": [str]}]
        return [
            {
                "value": slot_name,
                "synonyms": synonyms[slot_name]
            }
            for slot_name in synonyms
            if len(synonyms[slot_name]) > 1
        ]

    @staticmethod
    def __find_entity(text, entity_str):
        """
        Finds the entity `entity_str` in `text`
        ignoring the case of the first non-space.
        """
        index = text.find((ENTITY_MARKER+entity_str).rstrip())
        if index == -1:
            return text.lower().find(entity_str.lower())
        return index


    def _get_base_to_extend(self):
        if self._base_file_contents is None:
            if self._base_filepath is None:
                return self._get_empty_base()
            with open(self._base_filepath, 'r') as base_file:
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
                "Couldn't load data from base file '" + \
                self._base_filepath + "'")
        else:
            if "rasa_nlu_data" not in self._base_file_contents:
                self._base_file_contents = None
                raise SyntaxError(
                    "Expected 'rasa_nlu_data' as a root of base file '" + \
                    self._base_filepath + "'")
            elif "common_examples" not in self._base_file_contents["rasa_nlu_data"] or \
                 "entity_synonyms" not in self._base_file_contents["rasa_nlu_data"]:
                    self._base_file_contents = None
                    raise SyntaxError(
                        "Expected at least 'entity_synonyms' and " + \
                        "'common_examples' inside 'rasa_nlu_data' " + \
                        "in base file '" + self._base_filepath + "'")
