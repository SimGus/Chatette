#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.unit_reference`
Contains a class representing all the references to unit definition
that are present in template rules.
"""


from chatette.refactor_units.generating_item import GeneratingItem


class UnitReference(GeneratingItem):
    """
    Represents a reference to a unit definition that can be contained
    in a template rule.
    """
    def __init__(self, name, unit_type, ast):
        # TODO there could be a better way to use ast (singleton?)
        super(UnitReference, self).__init__(name)
        self._unit_type = unit_type
        self._definition = ast.get_definition(unit_type, name)
    
    def _compute_full_name(self):
        return "reference to " + self._unit_type.name + " '" + \
            self._labelling_name + "'"
    
    def _compute_nb_possibilities(self):
        return self._definition.get_max_nb_possibilities()
    
    def _generate_random_strategy(self):
        return self._definition.generate_random()
    
    def _generate_all_strategy(self):
        return self._definition.generate_all()
    
    def _generate_n_strategy(self, n):
        return self._definition.generate_nb_possibilities(n)
