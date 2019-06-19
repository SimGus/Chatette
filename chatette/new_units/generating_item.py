#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.generating_item`
Contains the abstract class that is the basis of
all unit definitions and rule contents.
"""


from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class GeneratingItem(with_metaclass(ABCMeta, object)):
    """
    Represents all items that can generate a string
    (and possibly meta-information such as entities or intent information).
    Each possibility of string that this item can generate is called
    a possibility or an example.
    """
    def __init__(self, name=None):
        self._labelling_name = name
        self.name = self._compute_full_name()
        self._total_nb_possibilities = None
        self.modifiers = None
    @abstractmethod
    def _compute_full_name(self):
        return NotImplementedError()

    def get_nb_possibilities(self):
        """
        Returns the number of possible string this item can generate,
        if this number was calculated before.
        If it wasn't, this should run the computation.
        """
        if self._total_nb_possibilities is None:
            self._compute_nb_possibilities()
        return self._total_nb_possibilities
    @abstractmethod
    def _compute_nb_possibilities(self):
        """Computes the number of possible strings this item can generate."""
        raise NotImplementedError()

    @abstractmethod
    def generate_nb_examples(self, nb_examples):
        """
        Generates `nb_examples` examples of the possibilities
        this item can generate, chosen at random.
        """
        raise NotImplementedError()
    def generate_random(self):
        """
        Generates one of the possibilies this item can generate,
        chosen at random.
        Usually, this internally calls `self.generate_nb_examples`.
        """
        return self.generate_nb_examples(1)
    def generate_all(self):
        """
        Generates all the possibilities this item can generate.
        Usually, this internally calls `self.generate_nb_examples`.
        """
        return self.generate_nb_examples(self.get_nb_possibilities())
