import io
import json
import os

from chatette.utils import cast_to_unicode
from chatette.units import ENTITY_MARKER
from ._base import Adapter


class JsonListAdapter(Adapter):

    def _get_file_extension(self):
        return "jsonl"

    def prepare_example(self, example):
        example.text = example.text.replace(ENTITY_MARKER, "")
        return json.dumps(cast_to_unicode(example.__dict__), ensure_ascii=False, sort_keys=True)

    def _write_batch(self, output_file_handle, batch):
        output_file_handle.writelines([
            self.prepare_example(example) + "\n"
            for example in batch.examples
        ])

    def write(self, output_directory, examples, synonyms):
        super(JsonListAdapter, self).write(output_directory, examples, synonyms)

        processed_synonyms = self.__synonym_format(synonyms)
        if processed_synonyms is not None:
            synonyms_file_path = os.path.join(output_directory, "synonyms.json")
            with io.open(synonyms_file_path, 'w') as output_file:
                output_file.write(json.dumps(cast_to_unicode(processed_synonyms),
                                             ensure_ascii=False,
                                             sort_keys=True, indent=2))


    @classmethod
    def __synonym_format(cls, synonyms):
        result = {key: values for (key, values)in synonyms.items()
                              if len(values) > 1 or values[0] != key}
        if not result:
            return None
        return result
