import os
import io
from collections import OrderedDict
import ruamel.yaml as yaml

from chatette.adapters._base import Adapter
from chatette.utils import append_to_list_in_dict, cast_to_unicode

def intent_dict_to_list_of_dict(data):
    list_data = []
    for key, values in data.items():
        list_data.append(
            {
                "intent": key,
                "examples": '\n'.join(['- ' + v for v in values]) + '\n'
            }
        )

    return list_data

class RasaYMLAdapter(Adapter):
    def __init__(self, base_filepath=None):
        super(RasaYMLAdapter, self).__init__(base_filepath, None)
        self._base_file_contents = None

    @classmethod
    def _get_file_extension(cls):
        return "yml"

    def __get_file_name(self, batch, output_directory, single_file):
        if single_file:
            return \
                os.path.join(
                    output_directory, "nlu." + self._get_file_extension()
                )
        raise ValueError(
            "Tried to generate several files with Rasa YAML adapter."
        )

    def _write_batch(self, output_file_handle, batch):
        data = self._get_base_to_extend()
        prepared_examples = dict()
        for example in batch.examples:
            append_to_list_in_dict(
                prepared_examples,
                example.intent_name, self.prepare_example(example)
            )
        prepared_examples = intent_dict_to_list_of_dict(prepared_examples)
        prepared_examples.extend(
            self.__format_synonyms(batch.synonyms)
        )
        data['nlu'] = prepared_examples
        data = cast_to_unicode(data)

        yaml.scalarstring.walk_tree(data)
        yaml.round_trip_dump(data, output_file_handle, default_flow_style=False, allow_unicode=True)


    def prepare_example(self, example):
        if len(example.entities) == 0:
            return example.text

        sorted_entities = \
            sorted(
                example.entities,
                reverse=True,
                key=lambda entity: entity._start_index
            )
        result = example.text[:]
        for entity in sorted_entities:
            entity_annotation_text = ']{"entity": "' + entity.slot_name
            entity_text = result[entity._start_index:entity._start_index + entity._len]
            if entity_text != entity.value:
                entity_annotation_text += f', "value": "{entity.value}'
            if entity.role is not None:
                entity_annotation_text += f', "role": "{entity.role}'
            if entity.group is not None:
                entity_annotation_text += f', "group": "{entity.group}'
            result = \
                result[:entity._start_index] + "[" + \
                entity_text + entity_annotation_text + '"}' + \
                result[entity._start_index + entity._len:] # New rasa entity format
        return result

    @classmethod
    def __format_synonyms(cls, synonyms):
        # {str: [str]} -> [{"value": str, "synonyms": [str]}]
        return [
            {
                "synonym": slot_name,
                "examples": '\n'.join(['- ' + s for s in synonyms[slot_name]]) + '\n'
            }
            for slot_name in synonyms
            if len(synonyms[slot_name]) > 1
        ]

    def _get_base_to_extend(self):
        ### TODO Implement later
        return self._get_empty_base()        
        # if self._base_file_contents is None:
        #     if self._base_filepath is None:
        #         return self._get_empty_base()
        #     with io.open(self._base_filepath, 'r', encoding='utf-8') as base_file:
        #         self._base_file_contents = json.load(base_file)
        #     self.check_base_file_contents()
        # return self._base_file_contents

    def _get_empty_base(self):
        return {
            "nlu": list()
        }