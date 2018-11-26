import io
import os
from abc import ABCMeta, abstractmethod as abstract_method
from typing import List, TextIO

from chatette.units.intent import IntentExample


class Batch:
    def __init__(self, index, examples, synonyms):
        super().__init__()
        self.index = index
        self.examples = examples
        self.synonyms = synonyms


class Adapter(metaclass=ABCMeta):

    def __init__(self, batch_size=10_000) -> None:
        super().__init__()
        self._batch_size = batch_size

    def write(self, output_directory, examples: List[IntentExample], synonyms) -> None:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for batch in self.__generate_batch(examples, synonyms, self._batch_size):
            output_file_path = self.__get_file_name(batch, output_directory)
            with io.open(output_file_path, 'w', encoding="utf-8") as output_file:
                self._write_batch(output_file, batch)

    @abstract_method
    def _get_file_extension(self):
        raise NotImplementedError()

    @abstract_method
    def _write_batch(self, output_file_handle: TextIO, batch: Batch) -> None:
        raise NotImplementedError()

    @classmethod
    def __generate_batch(cls, examples, synonyms, n=1):
        length = len(examples)
        for index, ndx in enumerate(range(0, length, n)):
            yield Batch(index, examples[ndx:min(ndx + n, length)], synonyms)

    def __get_file_name(self, batch, output_directory):
        return os.path.join(output_directory, "output." + str(batch.index) + "." + self._get_file_extension())