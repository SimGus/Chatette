#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.unit_definitions.slot`
Contains the class representing a definition of a slot (i.e. an entity),
as it will be contained in the AST created by the parser.
"""


from chatette.new_units.unit_definitions import UnitDefinition


class SlotDefinition(UnitDefinition):
    """
    Represents the definition of a slot (i.e. an entity)
    as defined in the template files.
    """
    def _compute_full_name(self):
        return "slot '" + self._labelling_name + "'"

    def generate_random(self):
        generated_exemple = super(SlotDefinition, self).generate_random()
        #TODO
