#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.word`
Contains the definition of words as contents of rules.
"""


from chatette.refactor_units import Example
from chatette.refactor_units.generating_item import GeneratingItem


class Word(GeneratingItem):
    """Represents a word as a content of a rule."""
    def __init__(self, name=None):
        super(Word, self).__init__(name)
        self.word = name

    def _compute_full_name(self):
        return "word '" + self._name + "'"
    
    def get_max_nb_possibilities(self):
        return 1
    def _compute_nb_possibilities(self):
        return 1
    
    def generate_random(self):
        return Example(self._name)
    def _generate_random_strategy(self):
        return Example(self._name)
    
    def generate_all(self):
        return [Example(self._name)]
    def _generate_all_strategy(self):
        return [Example(self._name)]
    
    def generate_nb_possibilities(self, nb_possibilities):
        return [Example(self._name)]
    def _generate_n_strategy(self, n):
        return [Example(self._name)]
