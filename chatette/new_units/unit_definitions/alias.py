#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.unit_definitions.alias`
Contains the class representing a definition of an alias,
as it will be contained in the AST created by the parser.
"""


# pylint: disable=redefined-builtin
from six.moves import range

from chatette.new_units.unit_definitions import UnitDefinition


class AliasDefinition(UnitDefinition):
    """
    Represents the definition of an alias as defined in the template files.
    """
    def _compute_full_name(self):
        return "alias '" + self._labelling_name + "'"
    
    def _compute_max_nb_possibilities(self):
        max_nb_possibilities = 0
        for rule in self.rules:
            max_nb_possibilities += rule.get_max_nb_possibilities()
        self._total_nb_possibilities_approximated = True
        return max_nb_possibilities
    

