#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.definitions.slot`
Contains the class representing a slot definition.
"""


from chatette.refactor_units import Entity
from chatette.refactor_units.definitions.unit_definition import UnitDefinition


class SlotDefinition(UnitDefinition):
    """Represents an slot definition."""
    def _compute_full_name(self):
        return "slot '" + self._name + "'"

    def _generate_random_strategy(self):
        generated_example = \
            super(SlotDefinition, self)._generate_random_strategy()
        generated_example.entities.append(
            Entity(self._name, len(generated_example.text))  # TODO value?
        )
        return generated_example
    
    def _generate_all_strategy(self):
        generated_examples = \
            super(SlotDefinition, self)._generate_all_strategy()
        for ex in generated_examples:
            ex.entities.append(
                Entity(self._name, len(ex.text))  # TODO value?
            )
