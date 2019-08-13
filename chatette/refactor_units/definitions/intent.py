#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.definitions.intent`
Contains the class representing an intent definition.
"""


from random import shuffle

from chatette.refactor_units import Example, add_example_no_dup
from chatette.refactor_units.definitions.unit_definition import UnitDefinition


class IntentDefinition(UnitDefinition):
    """Represents an intent definition."""
    def __init__(
        self, name, nb_training_examples=None, nb_testing_examples=None
    ):
        super(IntentDefinition, self).__init__(name)
        self._nb_training_ex_asked = nb_training_examples
        self._nb_testing_ex_asked = nb_testing_examples
    
    def _compute_full_name(self):
        return "intent '" + self._name + "'"
    
    def set_nb_examples_asked(self, nb_training_ex, nb_testing_ex):
        """
        Sets the number of examples for this intent
        that should be in the training and test set.
        """
        self._nb_training_ex_asked = nb_training_ex
        self._nb_testing_ex_asked = nb_testing_ex
    
    def get_nb_training_examples_asked(self):
        return self._nb_training_ex_asked
    def get_nb_testing_examples_asked(self):
        return self._nb_testing_ex_asked

    
    def generate_train(self):
        """
        Returns a list of examples to make up the training set.
        The list has as many examples as were asked in teh templates.
        """
        if self._nb_training_ex_asked == 0:
            return Example()
        return self.generate_nb_possibilities(self._nb_training_ex_asked)
    def generate_test(self, training_examples):
        """
        Returns a list of examples that can be put in the test set
        (not present in the training set).
        The list has as many examples as were asked in the templates.
        """
        if self._nb_testing_ex_asked == 0:
            return Example()
        if (
            self._nb_testing_ex_asked < \
            float(self.get_max_nb_possibilities()) / 5.0
        ):
            test_examples = []
            loop_count = 0
            while len(test_examples) < self._nb_testing_ex_asked:
                current_ex = self.generate_random()
                add_example_no_dup(test_examples, current_ex)
                loop_count += 1
                if loop_count > 10*self._nb_testing_ex_asked:
                    break
            return test_examples
        else:
            test_examples = []
            all_examples = shuffle(self.generate_all())
            for ex in all_examples:
                add_example_no_dup(test_examples, ex)
                if len(test_examples) == self._nb_testing_ex_asked:
                    break
            return test_examples
