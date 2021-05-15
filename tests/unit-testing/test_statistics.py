# coding: utf-8
"""
Test module.
Tests the functions and classes in module 'chatette.utils'.
"""

import pytest

from chatette.statistics import Stats, InvalidStatsState
from chatette.utils import UnitType


class TestStats(object):
    def test_singleton(self):
        first = Stats.get_or_create()
        second = Stats.get_or_create()
        assert first == second
        reset = Stats.reset_instance()
        assert first != reset

    def test_init(self):
        instance = Stats.reset_instance()
        assert hasattr(instance, "nb_input_files_parsed")
        assert instance.nb_input_files_parsed == 0
        assert hasattr(instance, "nb_units_declared")
        assert instance.nb_units_declared == 0
        assert hasattr(instance, "nb_intents_declared")
        assert instance.nb_intents_declared == 0
        assert hasattr(instance, "nb_slots_declared")
        assert instance.nb_slots_declared == 0
        assert hasattr(instance, "nb_aliases_declared")
        assert instance.nb_aliases_declared == 0
        assert hasattr(instance, "nb_variation_units")
        assert instance.nb_variation_units == 0
        assert hasattr(instance, "nb_variation_intents")
        assert instance.nb_variation_intents == 0
        assert hasattr(instance, "nb_variation_slots")
        assert instance.nb_variation_slots == 0
        assert hasattr(instance, "nb_variation_aliases")
        assert instance.nb_variation_aliases == 0
        assert hasattr(instance, "nb_rules_parsed")
        assert instance.nb_rules_parsed == 0

    def test_str(self):
        str_repr = str(Stats.reset_instance())
        assert "Statistics:" in str_repr
        assert "Parsed files: 0" in str_repr
        assert "Declared units: 0 (0 variations)" in str_repr
        assert "Declared intents: 0 (0 variations)" in str_repr
        assert "Declared slots: 0 (0 variations)" in str_repr
        assert "Declared aliases: 0 (0 variations)" in str_repr
        assert "Parsed rules: 0" in str_repr

    def test_new_file(self):
        instance = Stats.reset_instance()
        assert instance.nb_input_files_parsed == 0
        instance.new_file_parsed()
        assert instance.nb_input_files_parsed == 1

    def test_new_units(self):
        instance = Stats.reset_instance()
        assert instance.nb_units_declared == 0
        assert instance.nb_intents_declared == 0
        assert instance.nb_slots_declared == 0
        assert instance.nb_aliases_declared == 0

        instance.new_unit_declared(UnitType.alias)
        assert instance.nb_units_declared == 1
        assert instance.nb_aliases_declared == 1

        instance.new_unit_declared(UnitType.slot)
        assert instance.nb_units_declared == 2
        assert instance.nb_slots_declared == 1

        instance.new_unit_declared(UnitType.intent)
        assert instance.nb_units_declared == 3
        assert instance.nb_intents_declared == 1

        with pytest.raises(TypeError):
            instance.new_unit_declared("invalid")

    def test_new_variations(self):
        instance = Stats.reset_instance()
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_intents == 0
        assert instance.nb_slots_declared == 0
        assert instance.nb_aliases_declared == 0

        instance.new_variation_unit_declared(UnitType.intent)
        assert instance.nb_variation_units == 1
        assert instance.nb_variation_intents == 1

        instance.new_variation_unit_declared(UnitType.slot)
        assert instance.nb_variation_units == 2
        assert instance.nb_variation_intents == 1

        instance.new_variation_unit_declared(UnitType.alias)
        assert instance.nb_variation_units == 3
        assert instance.nb_variation_aliases == 1

        with pytest.raises(TypeError):
            instance.new_variation_unit_declared("invalid")

    def test_new_rule(self):
        instance = Stats.reset_instance()
        assert instance.nb_rules_parsed == 0

        instance.new_rule_parsed()
        assert instance.nb_rules_parsed == 1

        instance.new_rule_parsed()
        assert instance.nb_rules_parsed == 2

    def test_new_rules(self):
        instance = Stats.reset_instance()
        assert instance.nb_rules_parsed == 0

        instance.new_rules_parsed(2)
        assert instance.nb_rules_parsed == 2

        instance.new_rules_parsed(5)
        assert instance.nb_rules_parsed == 7

    def test_remove_unit(self):
        instance = Stats.reset_instance()
        assert instance.nb_units_declared == 0
        assert instance.nb_intents_declared == 0
        assert instance.nb_slots_declared == 0
        assert instance.nb_aliases_declared == 0

        instance.new_unit_declared(UnitType.alias)
        instance.one_unit_removed(UnitType.alias)
        assert instance.nb_units_declared == 0
        assert instance.nb_aliases_declared == 0

        instance.new_unit_declared(UnitType.slot)
        instance.one_unit_removed(UnitType.slot)
        assert instance.nb_units_declared == 0
        assert instance.nb_slots_declared == 0

        instance.new_unit_declared(UnitType.intent)
        instance.one_unit_removed(UnitType.intent)
        assert instance.nb_units_declared == 0
        assert instance.nb_intents_declared == 0

        with pytest.raises(TypeError):
            instance.one_unit_removed("invalid")

        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.alias)
        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.slot)
        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.intent)

        instance.new_unit_declared(UnitType.alias)
        instance.nb_aliases_declared = 0
        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.alias)

        instance.new_unit_declared(UnitType.slot)
        instance.nb_slots_declared = 0
        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.slot)

        instance.new_unit_declared(UnitType.intent)
        instance.nb_intents_declared = 0
        with pytest.raises(InvalidStatsState):
            instance.one_unit_removed(UnitType.intent)

    def test_remove_variation(self):
        instance = Stats.reset_instance()
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_intents == 0
        assert instance.nb_variation_slots == 0
        assert instance.nb_variation_aliases == 0

        instance.new_variation_unit_declared(UnitType.alias)
        instance.one_variation_unit_removed(UnitType.alias)
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_aliases == 0

        instance.new_variation_unit_declared(UnitType.slot)
        instance.one_variation_unit_removed(UnitType.slot)
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_slots == 0

        instance.new_variation_unit_declared(UnitType.intent)
        instance.one_variation_unit_removed(UnitType.intent)
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_intents == 0

        with pytest.raises(TypeError):
            instance.one_variation_unit_removed("invalid")

        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.alias)
        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.slot)
        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.intent)

        instance.new_variation_unit_declared(UnitType.alias)
        instance.nb_variation_aliases = 0
        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.alias)

        instance.new_variation_unit_declared(UnitType.slot)
        instance.nb_variation_slots = 0
        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.slot)

        instance.new_variation_unit_declared(UnitType.intent)
        instance.nb_variation_intents = 0
        with pytest.raises(InvalidStatsState):
            instance.one_variation_unit_removed(UnitType.intent)

    def test_remove_variations(self):
        instance = Stats.reset_instance()
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_intents == 0
        assert instance.nb_variation_slots == 0
        assert instance.nb_variation_aliases == 0

        for _ in range(3):
            instance.new_variation_unit_declared(UnitType.alias)
        instance.several_variation_units_removed(UnitType.alias, 3)
        assert instance.nb_variation_units == 0
        assert instance.nb_variation_aliases == 0

    def test_remove_rules(self):
        instance = Stats.reset_instance()
        instance.new_rules_parsed(5)
        assert instance.nb_rules_parsed == 5

        instance.one_rule_removed()
        assert instance.nb_rules_parsed == 4

        instance.several_rules_removed(4)
        assert instance.nb_rules_parsed == 0

        with pytest.raises(InvalidStatsState):
            instance.one_rule_removed()
        with pytest.raises(InvalidStatsState):
            instance.several_rules_removed(2)
