import os
import io
from collections import OrderedDict
import ruamel.yaml as yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from ruamel.yaml.error import YAMLError
from ruamel.yaml.constructor import DuplicateKeyError

from chatette.adapters._base import Adapter
from chatette.utils import append_to_list_in_dict, cast_to_unicode

YAML_VERSION = (1, 2)

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

def fix_yaml_loader() -> None:
    """Ensure that any string read by yaml is represented as unicode."""
    """Code from Rasa yaml reader"""
    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    yaml.Loader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)
    yaml.SafeLoader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)


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
                entity_annotation_text += '", "value": "{}'.format(entity.value)
            if entity.role is not None:
                entity_annotation_text += '", "role": "{}'.format(entity.role)
            if entity.group is not None:
                entity_annotation_text += '", "group": "{}'.format(entity.group)
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

    def _read_yaml(self, content):
        fix_yaml_loader()
        yaml_parser = yaml.YAML(typ='safe')
        yaml_parser.version = YAML_VERSION
        yaml_parser.preserve_quotes = True
        yaml.allow_duplicate_keys = False

        return yaml_parser.load(content)

    def _get_base_to_extend(self):
        if self._base_file_contents is None:
            if self._base_filepath is None:
                return self._get_empty_base()
            with io.open(self._base_filepath, 'r', encoding='utf-8') as base_file:
                try:
                    self._base_file_contents = self._read_yaml(base_file.read())
                except (YAMLError, DuplicateKeyError) as e:
                    raise YamlSyntaxException(self._base_filepath, e) 
            self.check_base_file_contents()
        return self._base_file_contents

    def _get_empty_base(self):
        base = OrderedDict()
        base['version'] = DoubleQuotedScalarString('2.0')
        base['nlu'] = list()
        return base

    def check_base_file_contents(self): 
        """
        Checks that `self._base_file_contents` contains well formatted NLU dictionary.
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
            if "nlu" not in self._base_file_contents:
                self._base_file_contents = None
                raise SyntaxError(
                    "Expected 'nlu' as a root of base file '" + \
                    self._base_filepath + "'")


class YamlSyntaxException(Exception):
    """Raised when a YAML file can not be parsed properly due to a syntax error."""
    """code from rasa.shared.exceptions.YamlSyntaxException"""

    def __init__(self, filename, underlying_yaml_exception):
        self.filename = filename
        self.underlying_yaml_exception = underlying_yaml_exception

    def __str__(self):
        if self.filename:
            exception_text = "Failed to read '{}'.".format(self.filename)
        else:
            exception_text = "Failed to read YAML."

        if self.underlying_yaml_exception:
            self.underlying_yaml_exception.warn = None
            self.underlying_yaml_exception.note = None
            exception_text += " {}".format(self.underlying_yaml_exception)

        if self.filename:
            exception_text = exception_text.replace(
                'in "<unicode string>"', 'in "{}"'.format(self.filename)
            )

        exception_text += (
            "\n\nYou can use https://yamlchecker.com/ to validate the "
            "YAML syntax of your file."
        )
        return exception_text