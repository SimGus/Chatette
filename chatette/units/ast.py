#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.units.ast`
Contains the data structure holding the Abstract Syntax Tree generated
when parsing the template files.
NOTE: this is not exactly an AST as it is not a tree, but it has the same
      purpose as an AST in a compiler, i.e. an intermediate representation
      of the parsed information used to generate the output.
"""


import chatette.parsing.parser_utils as pu
from chatette.parsing.statistics import Stats


class AST(object):
    instance = None
    def __init__(self, master_filename):
        self.alias_definitions = dict()
        self.slot_definitions = dict()
        self.intent_definitions = dict()

        self.stats = Stats(master_filename)
    @staticmethod
    def get_or_create(master_filename):
        if AST.instance is None:
            AST.instance = AST(master_filename)
        return AST.instance

    def _get_relevant_dict(self, unit_type):
        """Returns the dict that stores units of type `unit_type`."""
        if unit_type == pu.UnitType.alias:
            return self.alias_definitions
        elif unit_type == pu.UnitType.slot:
            return self.slot_definitions
        elif unit_type == pu.UnitType.intent:
            return self.intent_definitions
        else:
            raise ValueError("Tried to get a definition with wrong type "+
                             "(expected alias, slot or intent)")


    def exists(self, definition_name, unit_type):
        """
        Returns `True` iff a unit of type `unit_type`
        with name `definition_name`.
        """
        return definition_name in self._get_relevant_dict(unit_type)
    def get_definition(self, definition_name, unit_type):
        """Returns the definition for unit with name `definition_name`."""
        relevant_dict = self._get_relevant_dict(unit_type)

        if definition_name not in relevant_dict:
            raise KeyError("Couldn't find a definition for " + unit_type.name +
                           " '" + definition_name + "' (did you mean to use " +
                           "the word group '[" + definition_name + "]'?)")

        return relevant_dict[definition_name]


    def add_unit(self, unit_type, unit_name, unit):
        """
        Adds the unit `unit` of type `unit_type` in the relevant dict.
        Raise a `ValueError` if the unit was already declared.
        """
        relevant_dict = self._get_relevant_dict(unit_type)

        if unit_name in relevant_dict:
            raise ValueError(unit_type.name.capitalize() + " '" + unit_name + \
                             "' was already declared.")

        relevant_dict[unit_name] = unit

    def add_rule_to_unit(self, unit_type, unit_name, variation_name, rule):
        """
        Adds the rule `rule` to the already declared unit `unit_name`.
        If it doesn't exist, raises a `ValueError`.
        """
        relevant_dict = self._get_relevant_dict(unit_type)

        if unit_name not in relevant_dict:
            raise ValueError("Tried to add a rule to the undeclared " + \
                             unit_type.name + ".")

        relevant_dict[unit_name].add_rule(rule, variation_name)


    def rename_unit(self, unit_type, old_name, new_name):
        """
        Renames the unit declaration of type `unit_type` from
        `old_name` to `new_name` (possibly replacing the unit with that name).
        Raises a `KeyError` if `old_name` is not a declared unit.
        WARNING: this can lead to inconsistent rules.
        """
        relevant_dict = self._get_relevant_dict(unit_type)

        if old_name in relevant_dict:
            if new_name in relevant_dict:
                raise ValueError("Tried to rename a definition to a name that " +
                                 "was already in use ('" + new_name + "').")
            relevant_dict[new_name] = relevant_dict[old_name]
            del relevant_dict[old_name]
            relevant_dict[new_name].name = new_name
        else:
            raise KeyError("No unit named '" + old_name + "' was found")

    def delete(self, unit_type, unit_name, variation_name=None):
        """Deletes a unit definition."""
        relevant_dict = self._get_relevant_dict(unit_type)
        if unit_type == pu.UnitType.alias:
            relevant_stat_decrement_function = self.stats.decrement_aliases
        elif unit_type == pu.UnitType.slot:
            relevant_stat_decrement_function = self.stats.decrement_slots
        elif unit_type == pu.UnitType.intent:
            relevant_stat_decrement_function = self.stats.decrement_intents

        if unit_name not in relevant_dict:
            raise KeyError("Couldn't find a definition for " + unit_type.name +
                           " '" + unit_name + "'.")

        nb_rules = relevant_dict[unit_name].get_nb_rules(variation_name)
        if variation_name is None:
            del relevant_dict[unit_name]
            relevant_stat_decrement_function()
            self.stats.decrement_declarations()
        else:
            relevant_dict[unit_name].delete_variation(variation_name)
        self.stats.remove_rules(nb_rules)

    def add_definition(self, unit_type, unit_name, definition):
        """Adds an already built definition to the list of declared units."""
        relevant_dict = self._get_relevant_dict(unit_type)
        if unit_type == pu.UnitType.alias:
            relevant_stat_increment_function = self.stats.increment_aliases
        elif unit_type == pu.UnitType.slot:
            relevant_stat_increment_function = self.stats.increment_slots
        elif unit_type == pu.UnitType.intent:
            relevant_stat_increment_function = self.stats.increment_intents

        if unit_name in relevant_dict:
            raise ValueError(unit_type.name.capitalize()+" '"+unit_name+"' " +
                             "is already defined. Tried to add a definition " +
                             "for it again.")

        relevant_dict[unit_name] = definition

        relevant_stat_increment_function()
        self.stats.increment_declarations()
        self.stats.add_rules(definition.get_nb_rules())


    def print_DBG(self):
        print("Aliases:")
        for alias_name in self.alias_definitions:
            self.alias_definitions[alias_name].print_DBG()
        print("Slots:")
        for slot_name in self.slot_definitions:
            self.slot_definitions[slot_name].print_DBG()
        print("Intents:")
        for intent_name in self.intent_definitions:
            self.intent_definitions[intent_name].print_DBG()
        print()
