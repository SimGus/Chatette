# coding: utf-8

"""
Module `chatette.refactor_units.modifiable.definitions.alias`
Contains the class representing an alias definition.
"""


from chatette.refactor_units.modifiable.definitions.unit_definition import \
    UnitDefinition


class AliasDefinition(UnitDefinition):
    """Represents an alias definition."""
    def _compute_full_name(self):
        return "alias '" + self._name + "'"
    