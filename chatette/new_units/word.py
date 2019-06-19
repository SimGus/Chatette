#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.word`
Contains the class representing a word as the content of a rule.
"""


from chatette.new_units.generating_item import GeneratingItem
from chatette.new_units import Example


class Word(GeneratingItem):
    """
    Represents a word in a rule, that can generate the word it identifies
    and that word only.
    """
    def __init__(self, name):
        super(Word, self).__init__(name)
        self.word = name
    def _compute_full_name(self):
        self.name = "word '" + self.word + "'"
    
    def _compute_nb_possibilities(self):
        return 1
    
    def generate_nb_possibilities(self, nb_examples):
        return Example(self.word)
