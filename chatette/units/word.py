#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.units.word`
Contains the definition of words as contents of rules.
"""


from chatette.units import Example
from chatette.units.generating_item import GeneratingItem


class Word(GeneratingItem):
    """Represents a word as a content of a rule."""
    def __init__(self, name, leading_space):
        super(Word, self).__init__(name, leading_space)
        self.word = name

    def _compute_full_name(self):
        return "word '" + self._name + "'"
    
    def get_max_nb_possibilities(self):
        return 1
    def _compute_nb_possibilities(self):
        return 1
    
    def generate_random(self, **kwargs):
        return self._generate_random_strategy()
    def _generate_random_strategy(self):
        if self._leading_space:
            return Example(' ' + self._name)
        return Example(self._name)
    
    def generate_all(self):
        return self._generate_all_strategy()
    def _generate_all_strategy(self):
        if self._leading_space:
            return [Example(' ' + self._name)]
        return [Example(self._name)]
    
    def generate_nb_possibilities(self, nb_possibilities):
        return self._generate_n_strategy()
    def _generate_n_strategy(self, n):
        if self._leading_space:
            return [Example(' ' + self._name)]
        return [Example(self._name)]
    
    def as_template_str(self):
        if self._leading_space:
            return ' ' + self.word
        return self.word
