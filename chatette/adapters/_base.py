# coding: utf-8
"""
Module `chatette.adapters._base`
Contains the definition of the superclass for all adapters and
for the batches of examples written to output files.
"""

import io
import os
import shutil

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
# pylint: disable=redefined-builtin
from six.moves import range


class Batch(object):
    """Represents one batch of examples to write in the output files."""
    def __init__(self, index, examples, synonyms):
        super(Batch, self).__init__()
        self.index = index
        self.examples = examples
        self.synonyms = synonyms


class Adapter(with_metaclass(ABCMeta, object)):
    """
    Superclass for all the adapters.
    Using the list of generated examples, creates and writes
    the output file(s).
    """
    def __init__(self, base_filepath=None, batch_size=10000):
        super(Adapter, self).__init__()
        self._batch_size = batch_size
        self._base_filepath = base_filepath

    def write(self, output_directory, examples, synonyms):
        """
        Creates files in `output/output_directory` and
        writes batches of the examples `examples` and synonyms `synonyms`
        into them.
        """
        if self._batch_size is not None:
            single_file_output = (len(examples) <= self._batch_size)
        else:
            single_file_output = True

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for batch in self.__generate_batch(examples, synonyms, self._batch_size):
            output_file_path = \
                self.__get_file_name(
                    batch, output_directory, single_file_output
                )
            with io.open(output_file_path, 'w') as output_file:
                self._write_batch(output_file, batch)

    @classmethod
    @abstractmethod
    def _get_file_extension(cls):
        raise NotImplementedError()
    def __get_file_name(self, batch, output_directory, single_file):
        # pylint: disable=bad-continuation
        if single_file:
            return \
                os.path.join(
                    output_directory, "output." + self._get_file_extension()
                )
        return \
            os.path.join(
                output_directory, "output." + str(batch.index) + "." + \
                self._get_file_extension()
            )


    @abstractmethod
    def _write_batch(self, output_file_handle, batch):
        """
        Writes a batch of examples to file `output_file_handle`.
        This file will not be accessed after being written.
        """
        raise NotImplementedError()

    @classmethod
    def __generate_batch(cls, examples, synonyms, nb_examples_per_batch):
        """
        Generates a batch every time it is called, containing
        `nb_examples_per_batch` of the examples `examples`
        and the synonyms `synonyms`.
        If `nb_examples_per_batch` is `None`,
        one batch containing all the examples will be generated.
        """
        if nb_examples_per_batch is None:
            yield Batch(0, examples[:], synonyms)
        else:
            length = len(examples)
            for (batch_index, i) in enumerate(
                range(0, length, nb_examples_per_batch)
            ):
                yield \
                    Batch(
                        batch_index,
                        examples[i:min(i + nb_examples_per_batch, length)],
                        synonyms
                    )

    
    @abstractmethod
    def prepare_example(self, example):
        """Transforms an example into a str writable to an output file."""
        raise NotImplementedError()

    def _get_base_to_extend(self):
        """
        Returns a representation of the base to extend when writing a file.
        This base is taken from a file given through command line options.
        The type of object returned and what to do with it depends on the
        concrete implementation of the adapter.
        Some adapters shouldn't accept an extendable base.
        """
        raise ValueError(
            self.__class__.__name__ + " does not support base files."
        )
