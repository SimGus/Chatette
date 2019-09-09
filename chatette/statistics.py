# coding: utf-8
"""
Module `chatette.statistics`
Contains the singleton that is meant to record statistics about the execution
of the program.
"""

from chatette.utils import Singleton, UnitType


class InvalidStatsState(Exception):
    pass


class Stats(Singleton):
    _instance = None
    def __init__(self):
        # File counts
        self.nb_input_files_parsed = 0
        # self.nb_output_files = 0

        # Unit counts
        self.nb_units_declared = 0
        self.nb_intents_declared = 0
        self.nb_slots_declared = 0
        self.nb_aliases_declared = 0
        # Variation counts
        self.nb_variation_units = 0
        self.nb_variation_intents = 0
        self.nb_variation_slots = 0
        self.nb_variation_aliases = 0

        # Rule counts
        self.nb_rules_parsed = 0
    
    def __str__(self):
        return \
            "Statistics:\n\tParsed files: " + str(self.nb_input_files_parsed) + \
            "\n\tDeclared units: " + str(self.nb_units_declared) + \
            " (" + str(self.nb_variation_units) + " variations)" + \
            "\n\t\tDeclared intents: " + str(self.nb_intents_declared) + \
            " (" + str(self.nb_variation_intents) + " variations)" + \
            "\n\t\tDeclared slots: " + str(self.nb_slots_declared) + \
            " (" + str(self.nb_variation_slots) + " variations)" + \
            "\n\t\tDeclared aliases: " + str(self.nb_aliases_declared) + \
            " (" + str(self.nb_variation_aliases) + " variations)" + \
            "\n\tParsed rules: " + str(self.nb_rules_parsed)
    
    def new_file_parsed(self):
        self.nb_input_files_parsed += 1
    # def new_file_written(self):
    #     self.nb_output_files += 1

    def new_unit_declared(self, unit_type):
        if unit_type == UnitType.alias:
            self.new_alias_declared()
        elif unit_type == UnitType.slot:
            self.new_slot_declared()
        elif unit_type == UnitType.intent:
            self.new_intent_declared()
        else:
            raise TypeError(
                "Tried to increase the statistics for unit declarations " + \
                "with an unknown unit type (" + str(unit_type) + ")."
            )
    def new_intent_declared(self):
        self.nb_units_declared += 1
        self.nb_intents_declared += 1
    def new_slot_declared(self):
        self.nb_units_declared += 1
        self.nb_slots_declared += 1
    def new_alias_declared(self):
        self.nb_units_declared += 1
        self.nb_aliases_declared += 1
    
    def new_variation_unit_declared(self, unit_type):
        if unit_type == UnitType.alias:
            self.new_variation_alias_declared()
        elif unit_type == UnitType.slot:
            self.new_variation_slot_declared()
        elif unit_type == UnitType.intent:
            self.new_variation_intent_declared()
        else:
            raise TypeError(
                "Tried to increase the statistics for a variation of " + \
                "unit declarations with an unknown unit type (" + \
                str(unit_type) + ")."
            )
    def new_variation_intent_declared(self):
        self.nb_variation_units += 1
        self.nb_variation_intents += 1
    def new_variation_slot_declared(self):
        self.nb_variation_units += 1
        self.nb_variation_slots += 1
    def new_variation_alias_declared(self):
        self.nb_variation_units += 1
        self.nb_variation_aliases += 1

    def new_rule_parsed(self):
        self.nb_rules_parsed += 1
    def new_rules_parsed(self, nb_rules):
        self.nb_rules_parsed += nb_rules
    
    def one_unit_removed(self, unit_type):
        if unit_type == UnitType.alias:
            self.one_alias_removed()
        elif unit_type == UnitType.slot:
            self.one_slot_removed()
        elif unit_type == UnitType.intent:
            self.one_intent_removed()
        else:
            raise TypeError(
                "Tried to increase the statistics for a variation of " + \
                "unit declarations with an unknown unit type (" + \
                str(unit_type) + ")."
            )
    def one_intent_removed(self):
        self.nb_units_declared -= 1
        if self.nb_units_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for unit declarations below 0."
            )
        self.nb_intents_declared -= 1
        if self.nb_intents_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for intent declarations below 0."
            )
    def one_slot_removed(self):
        self.nb_units_declared -= 1
        if self.nb_units_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for unit declarations below 0."
            )
        self.nb_slots_declared -= 1
        if self.nb_slots_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for slot declarations below 0."
            )
    def one_alias_removed(self):
        self.nb_units_declared -= 1
        if self.nb_units_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for unit declarations below 0."
            )
        self.nb_aliases_declared -= 1
        if self.nb_aliases_declared < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for alias declarations below 0."
            )

    def several_variation_units_removed(self, unit_type, nb_variations):
        for _ in range(nb_variations):
            self.one_variation_unit_removed(unit_type)
    def one_variation_unit_removed(self, unit_type):
        if unit_type == UnitType.alias:
            self.one_variation_alias_removed()
        elif unit_type == UnitType.slot:
            self.one_variation_slot_removed()
        elif unit_type == UnitType.intent:
            self.one_variation_intent_removed()
        else:
            raise TypeError(
                "Tried to increase the statistics for a variation of " + \
                "unit declarations with an unknown unit type (" + \
                str(unit_type) + ")."
            )
    def one_variation_intent_removed(self):
        self.nb_variation_units -= 1
        if self.nb_variation_units < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "unit declarations below 0."
            )
        self.nb_variation_intents -= 1
        if self.nb_variation_intents < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "intent declarations below 0."
            )
    def one_variation_slot_removed(self):
        self.nb_variation_units -= 1
        if self.nb_variation_units < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "unit declarations below 0."
            )
        self.nb_variation_slots -= 1
        if self.nb_variation_slots < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "slot declarations below 0."
            )
    def one_variation_alias_removed(self):
        self.nb_variation_units -= 1
        if self.nb_variation_units < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "unit declarations below 0."
            )
        self.nb_variation_aliases -= 1
        if self.nb_variation_aliases < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for variations of " + \
                "alias declarations below 0."
            )

    def one_rule_removed(self):
        self.nb_rules_parsed -= 1
        if self.nb_rules_parsed < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for parsed rules below 0."
            )
    def several_rules_removed(self, nb_rules):
        self.nb_rules_parsed -= nb_rules
        if self.nb_rules_parsed < 0:
            raise InvalidStatsState(
                "Tried to decrement statistics for parsed rules below 0."
            )
        