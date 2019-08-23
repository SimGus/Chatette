# coding: utf-8
"""
Module `chatette.refactor_units.modifiable.definitions.intent`
Contains the class representing an intent definition.
"""

from random import shuffle

from chatette.utils import UnitType
from chatette.refactor_units import Example, IntentExample, add_example_no_dup
from chatette.refactor_units.modifiable.definitions.unit_definition import \
    UnitDefinition


class IntentDefinition(UnitDefinition):
    """Represents an intent definition."""
    unit_type = UnitType.intent
    def __init__(
        self, identifier, modifiers,
        nb_training_examples=None, nb_testing_examples=None
    ):
        super(IntentDefinition, self).__init__(identifier, modifiers)
        self._nb_training_ex_asked = nb_training_examples
        self._nb_testing_ex_asked = nb_testing_examples
        print(self.full_name + " TRAIN: " + str(self._nb_training_ex_asked) + " TEST: " + str(self._nb_testing_ex_asked))
    
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


    def _make_empty_example(self):
        return IntentExample(self._name)

    def _example_to_intent_example(self, example):
        """
        Turns the example `example` (of type `Example`) into an instance of
        `IntentExample`.
        """
        return IntentExample.from_example(example, self._name)

    
    def _generate_random_strategy(self, variation_name=None):
        example = \
            super(IntentDefinition, self) \
                ._generate_random_strategy(variation_name=variation_name)
        return self._example_to_intent_example(example)
    
    def _generate_all_strategy(self, variation_name=None):
        examples = \
            super(IntentDefinition, self) \
                ._generate_all_strategy(variation_name=variation_name)
        return [self._example_to_intent_example(ex) for ex in examples]

    
    def generate_train(self):
        """
        Returns a list of examples to make up the training set.
        The list has as many examples as were asked in teh templates.
        """
        if self._nb_training_ex_asked is None:
            return self.generate_all()
        if self._nb_training_ex_asked == 0:
            return []
        return self.generate_nb_possibilities(self._nb_training_ex_asked)

    def generate_test(self, training_examples):
        """
        Returns a list of examples that can be put in the test set
        (not present in the training set).
        The list has as many examples as were asked in the templates.
        """
        if self._nb_testing_ex_asked is None or self._nb_testing_ex_asked == 0:
            return []
        if (
            self._nb_testing_ex_asked < \
            float(self.get_max_nb_possibilities()) / 5.0
        ):
            test_examples = []
            loop_count = 0
            while len(test_examples) < self._nb_testing_ex_asked:
                loop_count += 1
                current_ex = self.generate_random()
                if current_ex in training_examples:
                    continue
                add_example_no_dup(test_examples, current_ex)

                if loop_count > 10*self._nb_testing_ex_asked:
                    break
            return test_examples
        else:
            test_examples = []
            all_examples = self.generate_all()
            shuffle(all_examples)
            for ex in all_examples:
                if ex in training_examples:
                    continue
                add_example_no_dup(test_examples, ex)

                if len(test_examples) == self._nb_testing_ex_asked:
                    break
            return test_examples
