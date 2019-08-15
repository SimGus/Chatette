# coding: utf-8
"""
Module `chatette.refactor_units.modifiable`
Contains all the classes representing items
whose generation can be modified by modifiers.
All those classes extend the abstract class `ModifiableItem`
which is a sub-class of `GeneratingItem`.
"""

from abc import abstractmethod
from random import choice, uniform
from copy import deepcopy

from chatette.refactor_units.generating_item import GeneratingItem
from chatette.refactor_units import Example


class ModifiableItem(GeneratingItem):
    def __init__(self, name, modifiers=None):
        super(ModifiableItem, self).__init__(name)
        self._modifiers_repr = modifiers
    
    def get_max_nb_possibilities(self):
        """
        Overriding.
        Calls the abstract method that computes the number of possibilities
        (without modifiers) and applies the modifiers.
        Caches the number of possibilities after computation.
        """
        if self._total_nb_possibilities is None:
            basic_nb_possibilities = self._compute_nb_possibilities()
            self._total_nb_possibilities = \
                ModifierApplier.modify_nb_possibilities(
                    basic_nb_possibilities, self._modifiers_repr
                )
        return self._total_nb_possibilities
    
    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_random(self):
        """Overriding."""
        if not ModifierApplier.should_generate():
            return Example()
        if (
            uniform(0, 1) <= \
            float(len(self._cached_examples)) / float(self.get_max_nb_possibilities())
        ):
            return choice(self._cached_examples)
        basic_example = self._generate_random_strategy()
        return ModifierApplier.apply_post_modifiers(basic_example)
    
    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_all(self):
        """Overriding."""
        if len(self._cached_examples) == 0:
            basic_examples = self._generate_all_strategy()
            self._cached_examples = ModifierApplier.apply_all_examples(basic_examples)
        return deepcopy(self._cached_examples)
