#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units.definitions.alias`
Contains the class representing an alias definition.
"""


from chatette.refactor_units.definitions.unit_definition import UnitDefinition


class AliasDefinition(UnitDefinition):
    """Represents an alias definition."""
    def _compute_full_name(self):
        return "alias '" + self._labelling_name + "'"
    