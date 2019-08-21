# coding: utf-8
"""
Module `chatette.refactor_units.modifiable.definitions.slot`
Contains the class representing a slot definition.
"""

from chatette.utils import UnitType
from chatette.refactor_units import Entity
from chatette.refactor_units.modifiable.definitions.unit_definition import \
    UnitDefinition


class SlotDefinition(UnitDefinition):
    """Represents an slot definition."""
    unit_type = UnitType.slot
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

    def get_synonyms_dict(self):
        # TODO find out what this was supposed to do in old code
        return dict()
