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
    