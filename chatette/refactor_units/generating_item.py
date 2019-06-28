#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.generating_item`
Contains the abstract class representing every item in the AST (or in rules)
that are able to generate examples.
"""


from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from random import uniform, choice
from copy import deepcopy


class GeneratingItem(with_metaclass(ABCMeta, object)):
    """
    Represents all items that are able to generate an example
    (i.e. a string with meta-information such as entities or intent information).
    Each possibility of string that this item can generate is called
    a possibility or an example.
    """
    def __init__(self, name=None):
        self._name = name
        self.full_name = self._compute_full_name()

        self._total_nb_possibilities = None

        # Cache: can contain a certain number of exampels previously generated
        self._cached_examples = []
    @abstractmethod
    def _compute_full_name(self):
        """
        Computes and returns the full name of the current item,
        that can be then displayed to the user.
        This name can be found in `self.full_name` after `__init__` was executed.
        """
        raise NotImplementedError()
    
    def get_max_nb_possibilities(self):
        """
        Returns the number of possible examples this item can generate.
        Uses the cached number of possibilities, or computes it.
        """
        if self._total_nb_possibilities is None:
            self._total_nb_possibilities = self._compute_nb_possibilities()
        return self._total_nb_possibilities
    @abstractmethod
    def _compute_nb_possibilities(self):
        """Returns the number of possible examples this item can generate."""
        raise NotImplementedError()
    

    def generate_random(self):
        """
        Returns an example generated at random.
        Can use the cached examples in some cases (better performance).
        """
        # use cache with probability `len(cached)/nb_possibilities`
        if uniform(0, 1) <= len(self._cached_examples)/self.get_max_nb_possibilities():
            return choice(self._cached_examples)
        return self._generate_random_strategy()
    @abstractmethod
    def _generate_random_strategy(self):
        """
        Strategy to generate one example at random without using the cache.
        Returns the generated example.
        """
        raise NotImplementedError()
    
    def generate_all(self):
        """
        Returns the list of all examples this item can generate.
        Can use the cached examples in some cases (better performance).
        Also sets up the cache if needed and fixes the count of possibilities.
        """
        if len(self._cached_examples) == self.get_max_nb_possibilities():
            return deepcopy(self._cached_examples)

        all_examples = self._generate_all_strategy()
        if len(self._cached_examples) == 0:
            # TODO don't cache it all in all cases
            self._cached_examples = deepcopy(all_examples)
            self._total_nb_possibilities = len(all_examples)
        return all_examples
    @abstractmethod
    def _generate_all_strategy(self):
        """
        Strategy to generate all possible examples without using the cache.
        Returns this list.
        """
        raise NotImplementedError()

    def generate_nb_possibilities(self, nb_possibilities):
        """
        Returns a list containing `nb_possibilities` examples,
        chosen at random in the set of all possible examples.
        Can use the cached examples in some cases (better performances).
        """
        raise NotImplementedError()
    @abstractmethod
    def _generate_n_strategy(self, n):
        """
        Strategy to generate `n` examples without using the cache.
        Returns the list of generated examples.
        """
        raise NotImplementedError()
