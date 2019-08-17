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

from chatette.modifiers import casegen, argument, randgen


class ModifiableItem(GeneratingItem):
    def __init__(self, name, leading_space, modifiers=None):
        super(ModifiableItem, self).__init__(name, leading_space)
        if modifiers is None:
            raise ValueError("Modifiers is none: " + self.__class__.__name__)
        self._modifiers_repr = modifiers


    def _make_empty_example(self):
        """
        Returns an example without any text or entity.
        Needed to be able to return a different type of example
        within intent definitions and other items.
        """
        return Example()

    
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
                self._modify_nb_possibilities(basic_nb_possibilities)
        return self._total_nb_possibilities
    

    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_random(self, **kwargs):
        """
        Overriding.
        `kwargs` can contain the random name mapping `randgen_mapping`.
        """
        randgen_mapping = kwargs.get("randgen_mapping", None)
        if not self._should_generate(randgen_mapping):
            return self._make_empty_example()
        if (
            uniform(0, 1) <= \
            float(len(self._cached_examples)) / float(self.get_max_nb_possibilities())
        ):
            return choice(self._cached_examples)
        basic_example = self._generate_random_strategy()
        if self._leading_space:
            basic_example.prepend(' ')
        return self._apply_modifiers(basic_example)
    

    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_all(self):
        """Overriding."""
        if len(self._cached_examples) == 0:
            basic_examples = self._generate_all_strategy()
            if self._leading_space:
                for ex in basic_examples:
                    ex.prepend(' ')
            self._cached_examples = \
                self._apply_modifiers_to_all(basic_examples)
        return deepcopy(self._cached_examples)
    

    def _modify_nb_possibilities(self, nb_possibilities):
        """
        Returns the number of possible different examples after application
        of the modifiers. `nb_possibilities` is the number of possibilities
        before the application of modifiers.
        """
        if self._modifiers_repr.casegen:
            nb_possibilities = \
                casegen.modify_nb_possibilities(nb_possibilities)
        if self._modifiers_repr.argument_value is not None:
            nb_possibilities = \
                argument.modify_nb_possibilities(nb_possibilities)
        return nb_possibilities
    

    def _should_generate(self, randgen_mapping):
        """
        Returns `True` iff the current object should generate one example
        given its pre-modifiers (namely, the case generation modifier).
        `randgen_mapping` is the mapping from random generation modifier names
        to their boolean value.
        """
        if self._modifiers_repr.randgen:
            return \
                randgen.should_generate(
                    self._modifiers_repr.randgen_name,
                    self._modifiers_repr.randgen_percent,
                    randgen_mapping
                )
        return True
    
    
    def _apply_modifiers(self, example):
        """
        Returns the modified `example`
        after its post-modifiers have been applied.
        """
        if self._modifiers_repr.casegen:
            example = casegen.modify_example(example)
        if self._modifiers_repr.argument_value is not None:
            example = \
                argument.modify_example(
                    example, self._modifiers_repr.argument_value
                )
        return example
    
    def _apply_modifiers_to_all(self, examples):
        """
        Returns the list of examples `examples` with some additional examples,
        some removed examples and some modified examples as per application
        of its post-modifiers.
        """
        print("bf modifiers: " + str(examples))
        print("randgen? " + str(self._modifiers_repr.randgen))
        if self._modifiers_repr.casegen:
            examples = casegen.make_all_possibilities(examples)
        if self._modifiers_repr.argument_value is not None:
            examples = \
                argument.make_all_possibilities(
                    examples, self._modifiers_repr.argument_value
                )
        if self._modifiers_repr.randgen:
            examples = \
                randgen.make_all_possibilities(
                    examples, self._make_empty_example()
                )
        print("after modifiers: " + str(examples))
        return examples
