# coding: utf-8
"""
Module `chatette.units.modifiable`
Contains all the classes representing items
whose generation can be modified by modifiers.
All those classes extend the abstract class `ModifiableItem`
which is a sub-class of `GeneratingItem`.
"""

from abc import abstractmethod
from random import choice as random_choice, uniform
from copy import deepcopy

from chatette.units.generating_item import GeneratingItem
from chatette.units import Example

from chatette.modifiers import casegen, argument, randgen


class ModifiableItem(GeneratingItem):
    def __init__(self, name, leading_space, modifiers):
        super(ModifiableItem, self).__init__(name, leading_space)
        if modifiers is None:
            raise ValueError(
                "Tried to instantiate a modifiable item " + \
                "with no modifier representation (" + \
                self.__class__.__name__ + ")"
            )
        self._modifiers_repr = modifiers
        # TODO add a check for modifiers


    def _make_empty_example(self):
        """
        Returns an example without any text or entity.
        Needed to be able to return a different type of example
        within intent definitions and other items.
        """
        return Example()


    def get_max_nb_possibilities(self, **kwargs):
        """
        Overriding.
        Calls the abstract method that computes the number of possibilities
        (without modifiers) and applies the modifiers.
        Caches the number of possibilities after computation.
        `kwargs` can contain `variation_name`.
        """
        if self._total_nb_possibilities is None:
            basic_nb_possibilities = self._compute_nb_possibilities(**kwargs)
            self._total_nb_possibilities = \
                self._modify_nb_possibilities(basic_nb_possibilities)
        return self._total_nb_possibilities


    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_random(self, **kwargs):
        """
        Overriding.
        `kwargs` can contain the random name mapping `randgen_mapping` or
        `variation_name`.
        """
        variation_name = kwargs.get("variation_name", None)

        randgen_mapping = kwargs.get("randgen_mapping", None)
        if not self._should_generate(randgen_mapping):
            return self._make_empty_example()

        if variation_name is not None:
            max_nb_possibilities = \
                self.get_max_nb_possibilities(variation_name=variation_name)
        else:
            max_nb_possibilities = self.get_max_nb_possibilities()
        if isinstance(self._cached_examples, list):
            if (
                len(self._cached_examples) > 0
                and uniform(0, 1) <= \
                float(len(self._cached_examples)) / float(max_nb_possibilities)
            ):
                return random_choice(deepcopy(self._cached_examples))
        else:
            pass  # TODO dict case for unit definitions with variations

        if variation_name is not None:
            basic_example = \
                self._generate_random_strategy(variation_name=variation_name)
        else:
            basic_example = self._generate_random_strategy()
        if self._leading_space:
            basic_example.prepend(' ')
        return self._apply_modifiers(basic_example)


    # TODO this is quite hacky to avoid code duplication in subclasses (and not use the decorator pattern to avoid having too many objects)
    def generate_all(self, **kwargs):
        """Overriding."""
        if len(self._cached_examples) < self.get_max_nb_possibilities():
            basic_examples = self._generate_all_strategy(**kwargs)
            if self._leading_space:
                for ex in basic_examples:
                    ex.prepend(' ')
            all_examples = self._apply_modifiers_to_all(basic_examples)
            if self.get_max_cache_size() > 0:
                self._cached_examples = deepcopy(all_examples)
            return all_examples
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
        if self._modifiers_repr.randgen:
            nb_possibilities = \
                randgen.modify_nb_possibilities(nb_possibilities)
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
                    self._modifiers_repr.randgen.name,
                    self._modifiers_repr.randgen.percentage,
                    self._modifiers_repr.randgen.opposite,
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
                    examples, self._make_empty_example(),
                    self._modifiers_repr.randgen.name,
                    self._modifiers_repr.randgen.opposite
                )
        return examples


    def set_arg_name(self, new_arg_name):
        """
        Changes the name of the argument modifier and uncaches everything.
        """
        self._modifiers_repr.argument_name = new_arg_name
        self._reset_caches()
    def set_arg_value(self, new_arg_value):
        """
        Changes the value of the argument modifier and uncaches everything.
        """
        self._modifiers_repr.argument_value = new_arg_value
        self._reset_caches()
    def set_casegen(self, new_casegen=True):
        """
        Changes the value of the casegen modifier and uncaches everything.
        """
        self._modifiers_repr.casegen = new_casegen
        self._reset_caches()
    def set_randgen(self, new_randgen=True):
        """
        Changes the value of the randgen modifier and uncaches everything.
        """
        self._modifiers_repr.randgen = new_randgen
        self._reset_caches()
    def set_randgen_name(self, new_randgen_name):
        """
        Changes the value of the randgen name modifier and uncaches everything.
        """
        self._modifiers_repr.randgen_name = new_randgen_name
        self._reset_caches()
    def set_randgen_percent(self, new_randgen_percent=50):
        """
        Changes the value of the randgen name modifier and uncaches everything.
        """
        self._modifiers_repr.randgen_percent = new_randgen_percent
