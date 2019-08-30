# coding: utf-8

"""
Module `chatette.units.modifiable.definitions.alias`
Contains the class representing an alias definition.
"""

from chatette.utils import UnitType
from chatette.units.modifiable.definitions.unit_definition import \
    UnitDefinition


class AliasDefinition(UnitDefinition):
    """Represents an alias definition."""
    unit_type = UnitType.alias
    def _compute_full_name(self):
        return "alias '" + self._name + "'"
    