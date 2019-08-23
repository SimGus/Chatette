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


    def _check_rule_validity(self, rule):
        """Override."""
        pass


    def _generate_random_strategy(self):
        generated_example = \
            super(SlotDefinition, self)._generate_random_strategy()
        
        slot_value = generated_example._slot_value
        if slot_value is None:
            slot_value = generated_example.text
        generated_example.entities.append(
            Entity(self._name, len(generated_example.text), slot_value)
        )
        generated_example._slot_value = None

        return generated_example
    
    def _generate_all_strategy(self):
        generated_examples = \
            super(SlotDefinition, self)._generate_all_strategy()
        
        for ex in generated_examples:
            slot_value = ex._slot_value
            if slot_value is None:
                slot_value = ex.text
            ex.entities.append(
                Entity(self._name, len(ex.text), slot_value)
            )
            ex._slot_value = None

        return generated_examples


    def get_synonyms_dict(self):
        # TODO find out what this was supposed to do in old code
        return dict()
