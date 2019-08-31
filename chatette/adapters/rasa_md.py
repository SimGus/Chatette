# coding: utf-8
"""
Module `chatette.adapters.rasa_md`
Contains the definition of the adapter that writes output in Markdown
for Rasa NLU.
"""

import os

from chatette.adapters._base import Adapter
from chatette.utils import append_to_list_in_dict, cast_to_unicode


class RasaMdAdapter(Adapter):
    def __init__(self, base_filepath=None):
        super(RasaMdAdapter, self).__init__(base_filepath, None)


    def _get_file_extension(self):
        return "md"
    def __get_file_name(self, batch, output_directory, single_file):
        if single_file:
            return \
                os.path.join(
                    output_directory, "nlu." + self._get_file_extension()
                )
        raise ValueError(
            "Tried to generate several files with Rasa Markdown adapter."
        )
        
    
    def _write_batch(self, output_file_handle, batch):
        prepared_examples = dict()
        for example in batch.examples:
            append_to_list_in_dict(
                prepared_examples,
                example.intent_name, self.prepare_example(example)
            )
        
        for intent_name in prepared_examples:
            output_file_handle.write(
                "## intent:" + cast_to_unicode(intent_name) + '\n'
            )
            for text in prepared_examples[intent_name]:
                output_file_handle.write(cast_to_unicode("- " + text + '\n'))
            output_file_handle.write(cast_to_unicode('\n'))
        
        output_file_handle.write(
            cast_to_unicode(self.__format_synonyms(batch.synonyms))
        )


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
            result = \
                result[:entity._start_index] + "[" + \
                result[entity._start_index:entity._start_index + entity._len] + \
                "](" + entity.slot_name + ")" + \
                result[entity._start_index + entity._len:]
        return result
    

    def __format_synonyms(self, synonyms):
        """
        Returns a str that will be written in the output files for all
        the synonyms `synonyms`.
        """
        result = ""
        for syn_name in synonyms:
            if len(synonyms[syn_name]) > 1:
                result += "## synonym:" + syn_name + '\n'
                for syn in synonyms[syn_name]:
                    if syn != syn_name:
                        result += "- " + syn + '\n'
                result += '\n'
        return result
