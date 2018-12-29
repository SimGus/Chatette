import io
import json
import os
# from typing import List, TextIO

from chatette.utils import cast_to_unicode
from chatette.units import ENTITY_MARKER
# from chatette.units.intent import IntentExample
from ._base import Adapter#, Batch


class JsonListAdapter(Adapter):

    def _get_file_extension(self):
        return "jsonl"

    @staticmethod
    def _prepare_example(example):
        example.text = example.text.replace(ENTITY_MARKER, "")
        return json.dumps(cast_to_unicode(example.__dict__), ensure_ascii=False, sort_keys=True)

    def _write_batch(self, output_file_handle, batch):
    #def _write_batch(self, output_file_handle: TextIO, batch: Batch) -> None:
        output_file_handle.writelines([
            JsonListAdapter._prepare_example(example) + "\n"
            for example in batch.examples
        ])

    def write(self, output_directory, examples, synonyms):
    #def write(self, output_directory, examples: List[IntentExample], synonyms) -> None:
        super(JsonListAdapter, self).write(output_directory, examples, synonyms)

        synonyms_file_path = os.path.join(output_directory, "synonyms.json")
        with io.open(synonyms_file_path, 'w', encoding="utf-8") as output_file:
            output_file.write(json.dumps(cast_to_unicode(synonyms), ensure_ascii=False,
                                         sort_keys=True, indent=2))
