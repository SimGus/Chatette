# coding: utf-8
"""
Module `chatette.adapters.rasa_md`
Contains the definition of the adapter that writes output in Markdown
for Rasa NLU.
"""

import os
import io
from six import string_types

from chatette import __version__
from chatette.adapters._base import Adapter
from chatette.utils import append_to_list_in_dict, cast_to_unicode


class RasaMdAdapter(Adapter):
    def __init__(self, base_filepath=None):
        super(RasaMdAdapter, self).__init__(base_filepath, None)
        self._base_file_contents = None


    @classmethod
    def _get_file_extension(cls):
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
        output_file_handle.write(
            "<!-- Generated using Chatette v" + cast_to_unicode(__version__) + \
            " -->\n\n"
        )

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

        remainder = self._get_base_to_extend()
        if remainder is not None:
            output_file_handle.write(cast_to_unicode(remainder) + '\n')


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
    

    @classmethod
    def __format_synonyms(cls, synonyms):
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
    

    def _get_base_to_extend(self):
        if self._base_file_contents is None:
            if self._base_filepath is None:
                return self._get_empty_base()
            with io.open(self._base_filepath, 'r') as base_file:
                self._base_file_contents = ''.join(base_file.readlines())
            self.check_base_file_contents()
        return self._base_file_contents

    def _get_empty_base(self):
        return ""
    
    def check_base_file_contents(self):
        if self._base_file_contents is None:
            return
        if not isinstance(self._base_file_contents, string_types):
            self._base_file_contents = None
            raise SyntaxError(
                "Couldn't load valid data from base file '" + \
                self._base_file_contents + "'"
            )
