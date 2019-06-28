#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.unit_definitions.unit_definition`
Contains the abstract class that is the basis of all unit definitions,
that is everything that will be contained in the AST created by the parser.
"""


from abc import abstractmethod
from random import sample

from chatette.utils import choose
from chatette.new_units.generating_item import GeneratingItem


class UnitDefinition(GeneratingItem):
    """
    Represents the definition of a unit (alias, slot or intent) that have been
    defined in the template files.
    """
    _MAX_LOOP_FACTOR = 5

    def __init__(self, name=None):
        super(UnitDefinition, self).__init__(name)
        self._rules = []
        self.variations = dict()


    def _compute_max_nb_possibilities(self):
        max_nb_possibilities = 0
        for rule in self.rules:
            max_nb_possibilities += rule.get_max_nb_possibilities()
        self._total_nb_possibilities_approximated = True
        return max_nb_possibilities

    
    def add_rule(self, rule, variation=None):
        """
        Adds the rule `rule` to the list of rules for this definition.
        If `variation` is not `None`, this adds the rule for the variation
        `variation`.
        Usually, his internally calls `self.add_rules`.
        """
        self.add_rules([rule], variation)
    @abstractmethod
    def add_rules(self, rules, variation=None):
        """
        Adds each of the rules in the list `rules` to this definition.
        If `variation` is not `None`, this adds the rules for the variation
        `variation`.
        """
        raise NotImplementedError()


    def generate_random(self):
        if not self.modifiers.should_generate():
            return Example()

        generated_example = choose(self._rules).generate_random()

        return self.modifiers.apply_post_modifiers(generated_example)

    def generate_nb_possibiltities(self, nb_examples):
        max_nb_possibilities = self.get_max_nb_possibilities()
        if nb_examples > max_nb_possibilities:
            nb_examples = max_nb_possibilities

        if nb_examples <= max_nb_possibilities/5:  # QUESTION: is 5 a good idea?
            generated_examples = set()
            for _ in range(nb_examples):
                i = 0
                while True:
                    new_example = self.generate_random()
                    if new_example not in generated_examples:
                        generated_examples.add(new_example)
                        break
                    if i > UnitDefinition._MAX_LOOP_FACTOR * max_nb_possibilities:
                        break
                    i += 1
            return generated_examples
        else:
            all_examples = self._generate_all_examples()
            return sample(all_examples, nb_examples)
    
    def _generate_all_examples(self):
        """
        Generates all the possible examples and returns them.
        Does only that and no change to the state of the instance,
        it is thus meant to be used only internally,
        users should rather use the method `generate_all`.
        """
        generated_examples = set()
        for rule in self._rules:
            generated_examples.update(rule.generate_all())
        return generated_examples
