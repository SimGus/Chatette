# coding: utf-8
"""
Module `chatette.units.modifiable.definitions.slot`
Contains the class representing a slot definition.
"""

from chatette.utils import UnitType, append_to_list_in_dict, extend_list_in_dict
from chatette.units import Entity
from chatette.units.modifiable.definitions.unit_definition import \
    UnitDefinition


class SlotDefinition(UnitDefinition):
    """Represents an slot definition."""
    unit_type = UnitType.slot
    def __init__(self, *args, **kwargs):
        super(SlotDefinition, self).__init__(*args, **kwargs)
        self._synonyms = None

    def _compute_full_name(self):
        return "slot '" + self._name + "'"


    def _check_rule_validity(self, rule):
        """Override."""
        pass


    def _generate_random_strategy(self, variation_name=None):
        generated_example = \
            super(SlotDefinition, self)._generate_random_strategy(
                variation_name=variation_name
            )
        
        slot_value = generated_example._slot_value
        if slot_value is None:
            slot_value = generated_example.text
        generated_example.entities.append(
            Entity(self._name, len(generated_example.text), slot_value)
        )
        generated_example._slot_value = None

        return generated_example
    
    def _generate_all_strategy(self, variation_name=None):
        generated_examples = \
            super(SlotDefinition, self)._generate_all_strategy(
                variation_name=variation_name
            )
        
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
        if self._synonyms is None:
            self._synonyms = dict()
            for rule in self._all_rules:
                texts = [ex.text for ex in rule.generate_all()]
                if rule.slot_value is None:
                    for text in texts:
                        append_to_list_in_dict(self._synonyms, text, text)
                else:
                    extend_list_in_dict(self._synonyms, rule.slot_value, texts)
        return self._synonyms
