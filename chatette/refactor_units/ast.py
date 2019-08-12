# coding: utf-8
"""
Module `chatette.refactor_units.ast`
Contains the data structure holding the Abstract Syntax Tree generated
when parsing the template files.
NOTE: this is not exactly an AST as it is not a tree, but it has the same
      purpose as an AST in a compiler, i.e. an intermediate representation
      of the parsed information used to generate the output.
"""

from chatette.utils import UnitType


class AST(object):
    instance = None
    def __init__(self):
        self._alias_definitions = dict()
        self._slot_definitions = dict()
        self._intent_definitions = dict()
    @staticmethod
    def get_or_create():
        if AST.instance is None:
            AST.instance = AST()
        return AST.instance


    def _get_relevant_dict(self, unit_type):
        """Returns the dict that stores units of type `unit_type`."""
        if unit_type == UnitType.alias:
            return self._alias_definitions
        elif unit_type == UnitType.slot:
            return self._slot_definitions
        elif unit_type == UnitType.intent:
            return self._intent_definitions
        else:
            raise ValueError("Tried to get a definition with wrong type "+
                             "(expected alias, slot or intent)")
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
            raise ValueError(
                "Invalid type of key: " + unit_type.__class__.__name__ + "."
            )
        return self._get_relevant_dict(unit_type)
    

    def add_alias(self, alias):
        """
        Adds the alias definition `alias` in the relevant dict.
        @raises: `ValueError` if the alias was already defined.
        """
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
    

    def print_DBG(self):
        print("Aliases:")
        for alias_name in self._alias_definitions:
            self._alias_definitions[alias_name].print_DBG()
        print("Slots:")
        for slot_name in self._slot_definitions:
            self._slot_definitions[slot_name].print_DBG()
        print("Intents:")
        for intent_name in self._intent_definitions:
            self._intent_definitions[intent_name].print_DBG()
        print()
