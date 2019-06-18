#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.parsing.statistics`
Contains the class definition storing stats about parsing.
"""


class Stats(object):
    """This class stores and manages the statistics of parsing."""
    NB_FILES_INDEX = "#files"
    NB_DECL_INDEX = "#declarations"
    NB_RULES_INDEX = "#rules"
    NB_INTENTS_INDEX = "#intents"
    NB_ALIASES_INDEX = "#aliases"
    NB_SLOTS_INDEX = "#slots"

    def __init__(self, master_filename="<master-file>"):
        self._stats = {Stats.NB_FILES_INDEX: 1, Stats.NB_DECL_INDEX: 0, Stats.NB_RULES_INDEX: 0,
                       Stats.NB_INTENTS_INDEX: 0, Stats.NB_ALIASES_INDEX: 0,
                       Stats.NB_SLOTS_INDEX: 0}
        self._filenames = set(master_filename)
    

    def get_as_dict(self):
        return self._stats.copy()
    
    def get_nb_files(self):
        return self._stats[Stats.NB_FILES_INDEX]
    def get_nb_declarations(self):
        return self._stats[Stats.NB_DECL_INDEX]
    def get_nb_rules(self):
        return self._stats[Stats.NB_RULES_INDEX]
    def get_nb_intents(self):
        return self._stats[Stats.NB_INTENTS_INDEX]
    def get_nb_aliases(self):
        return self._stats[Stats.NB_ALIASES_INDEX]
    def get_nb_slots(self):
        return self._stats[Stats.NB_SLOTS_INDEX]


    def new_file(self, filename):
        """
        Returns `True` if the file named `filename` wasn't already parsed
        and update the statistics accordingly.
        Returns `False` otherwise.
        """
        if filename not in self._filenames:
            self._filenames.add(filename)
            self._stats[Stats.NB_FILES_INDEX] += 1
            return True
        return False

    def increment_declarations(self):
        self._stats[Stats.NB_DECL_INDEX] += 1
    def increment_rules(self):
        self._stats[Stats.NB_RULES_INDEX] += 1
    def increment_intents(self):
        self._stats[Stats.NB_INTENTS_INDEX] += 1
    def increment_aliases(self):
        self._stats[Stats.NB_ALIASES_INDEX] += 1
    def increment_slots(self):
        self._stats[Stats.NB_SLOTS_INDEX] += 1

    def decrement_declarations(self):
        if self._stats[Stats.NB_DECL_INDEX] <= 0:
            raise ValueError("Tried to decrement statistics for declarations below 0")
        self._stats[Stats.NB_DECL_INDEX] -= 1
    def decrement_rules(self):
        if self._stats[Stats.NB_RULES_INDEX] <= 0:
            raise ValueError("Tried to decrement statistics for rules below 0")
        self._stats[Stats.NB_RULES_INDEX] -= 1
    def decrement_intents(self):
        if self._stats[Stats.NB_INTENTS_INDEX] <= 0:
            raise ValueError("Tried to decrement statistics for intents below 0")
        self._stats[Stats.NB_INTENTS_INDEX] -= 1
    def decrement_aliases(self):
        if self._stats[Stats.NB_ALIASES_INDEX] <= 0:
            raise ValueError("Tried to decrement statistics for aliases below 0")
        self._stats[Stats.NB_ALIASES_INDEX] -= 1
    def decrement_slots(self):
        if self._stats[Stats.NB_SLOTS_INDEX] <= 0:
            raise ValueError("Tried to decrement statistics for slots below 0")
        self._stats[Stats.NB_SLOTS_INDEX] -= 1

    def add_rules(self, nb_new_rules):
        self._stats[Stats.NB_RULES_INDEX] += nb_new_rules
    def remove_rules(self, nb_rules_to_remove):
        if nb_rules_to_remove > self._stats[Stats.NB_RULES_INDEX]:
            raise ValueError("Tried to decrease statistics for rules below 0")
        self._stats[Stats.NB_RULES_INDEX] -= nb_rules_to_remove
