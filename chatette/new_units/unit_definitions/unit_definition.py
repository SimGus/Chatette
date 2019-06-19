#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.new_units.unit_definitions.unit_definition`
Contains the abstract class that is the basis of all unit definitions,
that is everything that will be contained in the AST created by the parser.
"""


from abc import abstractmethod

from chatette.new_units.generating_item import GeneratingItem


class UnitDefinition(GeneratingItem):
    """
    Represents the definition of a unit (alias, slot or intent) that have been
    defined in the template files.
    """
    def __init__(self, name=None):
        super(UnitDefinition, self).__init__(name)
        self.rules = []
        self.variations = dict()
    
    def add_rule(self, rule, variation=None):
        """
        Adds the rule `rule` to the list of rules for this definition.
        If `variation` is not `None`, this adds the rule for the variation
        `variation`.
        Usually, his internally calls `self.add_rules`.
        """
        self.add_rules([rule], variation)
    @abstractmethod
    def add_rules(self, rules, variation=None):
        """
        Adds each of the rules in the list `rules` to this definition.
        If `variation` is not `None`, this adds the rules for the variation
        `variation`.
        """
        raise NotImplementedError()
