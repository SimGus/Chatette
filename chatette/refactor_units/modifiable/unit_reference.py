# coding: utf-8
"""
Module `chatette.refactor_units.modifiable.unit_reference`
Contains a class representing all the references to unit definition
that are present in template rules.
"""

from chatette.refactor_units.modifiable import ModifiableItem
from chatette.refactor_units.ast import AST


class UnitReference(ModifiableItem):
    """
    Represents a reference to a unit definition that can be contained
    in a template rule.
    """
    def __init__(self, identifier, unit_type, leading_space, modifiers):
        self._unit_type = unit_type
        super(UnitReference, self).__init__(
            identifier, leading_space, modifiers
        )
        try:
            self._definition = AST.get_or_create()[unit_type][identifier]
        except KeyError:
            self._definition = None
        
    
    def _compute_full_name(self):
        return "reference to " + self._unit_type.value + " '" + \
            self._name + "'"
    

    def get_definition(self):
        if self._definition is None:
            try:
                self._definition = \
                    AST.get_or_create()[self._unit_type][self._name]
            except KeyError:
                raise KeyError(
                    "Couldn't find the definition corresponding to " + \
                    self.full_name + "."
                )
        return self._definition

    
    def _compute_nb_possibilities(self):
        return self.get_definition().get_max_nb_possibilities()
    
    def _generate_random_strategy(self):
        return self.get_definition().generate_random()
    
    def _generate_all_strategy(self):
        return self.get_definition().generate_all()
    
    def _generate_n_strategy(self, n):
        return self.get_definition().generate_nb_possibilities(n)
