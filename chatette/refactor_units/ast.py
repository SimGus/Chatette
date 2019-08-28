# coding: utf-8
"""
Module `chatette.refactor_units.ast`
Contains the data structure holding the Abstract Syntax Tree generated
when parsing the template files.
NOTE: this is not exactly an AST as it is not a tree, but it has the same
      purpose as an AST in a compiler, i.e. an intermediate representation
      of the parsed information used to generate the output.
"""

from chatette.utils import Singleton, UnitType
from chatette.statistics import Stats

from chatette.refactor_units.modifiable.definitions.alias import \
    AliasDefinition
from chatette.refactor_units.modifiable.definitions.slot import \
    SlotDefinition
from chatette.refactor_units.modifiable.definitions.intent import \
    IntentDefinition


class AST(Singleton):
    _instance = None
    def __init__(self):
        self._alias_definitions = dict()
        self._slot_definitions = dict()
        self._intent_definitions = dict()
    

    def _get_relevant_dict(self, unit_type):
        """Returns the dict that stores units of type `unit_type`."""
        if unit_type == UnitType.alias:
            return self._alias_definitions
        elif unit_type == UnitType.slot:
            return self._slot_definitions
        elif unit_type == UnitType.intent:
            return self._intent_definitions
        else:
            raise TypeError(
                "Tried to get a definition with wrong type " + \
                "(expected alias, slot or intent)"
            )
    def __getitem__(self, unit_type):
        """
        Returns the dictionary requested.
        `unit_type` can be either a str ("alias", "slot" or "intent")
        or a `UnitType`.
        @raises: - `KeyError` if `unit_type` is an invalid str.
                 - `ValueError` if `unit_type´ is neither a str or a `UnitType`.
        """
        if isinstance(unit_type, str):
            if unit_type == UnitType.alias.value:
                unit_type = UnitType.alias
            elif unit_type == UnitType.slot.value:
                unit_type = UnitType.slot
            elif unit_type == UnitType.intent.value:
                unit_type = UnitType.intent
            else:
                raise KeyError(
                    "Invalid key for the AST: '" + unit_type + "'."
                )
        elif not isinstance(unit_type, UnitType):
            raise TypeError(
                "Invalid type of key: " + unit_type.__class__.__name__ + "."
            )
        return self._get_relevant_dict(unit_type)
    

    def _add_unit(self, unit_type, unit):
        """
        Adds the intent definition `intent` in the relevant dict.
        @raises: `ValueError` if the intent was already defined.
        """
        relevant_dict = self._get_relevant_dict(unit_type)
        if unit.identifier in relevant_dict:
            raise ValueError(
                "Tried to declare " + unit_type.value + " '" + \
                unit.identifier + "' twice."
            )
        relevant_dict[unit.identifier] = unit

    def add_alias(self, alias):
        """
        Adds the alias definition `alias` in the relevant dict.
        @raises: `ValueError` if the alias was already defined.
        """
        # NOTE there might be a better way to check that the alias is not already defined without needing to call `get_relevant_dict`
        self._add_unit(UnitType.alias, alias)
        
    def add_slot(self, slot):
        """
        Adds the slot definition `slot` in the relevant dict.
        @raises: `ValueError` if the slot was already defined.
        """
        self._add_unit(UnitType.slot, slot)

    def add_intent(self, intent):
        """
        Adds the intent definition `intent` in the relevant dict.
        @raises: `ValueError` if the intent was already defined.
        """
        self._add_unit(UnitType.intent, intent)

    def add_unit(self, unit, unit_type=None):
        """
        Adds the unit definition `unit` in the relevant dict.
        If `unit_type` is `None`, detects the type of the definition
        by itself.
        @raises: - `TypeError` if the unit type is of an invalid type.
                 - `ValueError` if the unit was already declared.
        """
        if unit_type is None:
            if isinstance(unit, AliasDefinition):
                unit_type = UnitType.alias
            elif isinstance(unit, SlotDefinition):
                unit_type = UnitType.slot
            elif isinstance(unit, IntentDefinition):
                unit_type = UnitType.intent
            else:
                raise TypeError(  # Should never happen
                    "Tried to add something else than a unit definition " + \
                    "to the AST."
                )
        self._add_unit(unit_type, unit)
    

    def rename_unit(self, unit_type, old_name, new_name):
        """
        Changes the name of the unit `old_name` to `new_name` if it exists.
        @raises: - `KeyError` if the unit of type `unit_type` and name
                   `unit_name` wasn't declared.
                 - `ValueError` if the unit with name `new_name` already
                   existed.
        """
        relevant_dict = self._get_relevant_dict(unit_type)
        if old_name not in relevant_dict:
            raise KeyError(
                "Tried to rename " + unit_type.name + " '" + old_name + \
                "', but it wasn't declared."
            )
        if new_name in relevant_dict:
            raise ValueError(
                "Tried to rename " + unit_type.name + " '" + old_name + \
                "' to '" + new_name + "', but this " + unit_type.name + \
                " already existed."
            )
        unit = relevant_dict[old_name]
        del relevant_dict[old_name]
        unit.set_identifier(new_name)
        relevant_dict[new_name] = unit
    
    def delete_unit(self, unit_type, unit_name, variation_name=None):
        """
        Deletes the declared unit `unit_name` of type `unit_type`.
        If `variation_name` is not `None`, only deletes this particular
        variation for this unit.
        @raises: - `KeyError` if the unit `unit_name` wasn't declared.
        """
        relevant_dict = self._get_relevant_dict(unit_type)
        if unit_name not in relevant_dict:
            raise KeyError(
                "Tried to delete " + unit_type.name + " '" + unit_name + \
                "', but it wasn't declared."
            )
        if variation_name is None:
            del relevant_dict[unit_name]
        else:
            relevant_dict[unit_name].delete_variation(variation_name)
    

    def print_DBG(self):
        print("Aliases (" + str(len(self._alias_definitions)) + "):")
        for alias_name in self._alias_definitions:
            self._alias_definitions[alias_name].print_DBG()
        print("Slots (" + str(len(self._slot_definitions)) + "):")
        for slot_name in self._slot_definitions:
            self._slot_definitions[slot_name].print_DBG()
        print("Intents (" + str(len(self._intent_definitions)) + "):")
        for intent_name in self._intent_definitions:
            self._intent_definitions[intent_name].print_DBG()
        print()
