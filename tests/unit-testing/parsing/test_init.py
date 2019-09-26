# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.parsing.__init__`.
"""

import pytest

from chatette.parsing import \
    ItemBuilder, ChoiceBuilder, UnitRefBuilder, \
    UnitDefBuilder, AliasDefBuilder, SlotDefBuilder, IntentDefBuilder

from chatette.utils import UnitType

from chatette.modifiers.representation import ModifiersRepresentation
from chatette.units.modifiable.choice import Choice
from chatette.units.modifiable.unit_reference import UnitReference
from chatette.units.modifiable.definitions.alias import AliasDefinition
from chatette.units.modifiable.definitions.slot import SlotDefinition
from chatette.units.modifiable.definitions.intent import IntentDefinition


class TestItemBuilder(object):
    def test_abstract(self):
        with pytest.raises(TypeError):
            ItemBuilder()


class TestChoiceBuilder(object):
    def test_creation(self):
        builder = ChoiceBuilder()
        assert not builder.leading_space
        assert not builder.casegen
        assert not builder.randgen
        assert builder.randgen_name is None
        assert builder.randgen_percent == 50

    def test_create_concrete(self):
        builder = ChoiceBuilder()
        builder.randgen_name = "name"

        with pytest.raises(ValueError):
            builder.create_concrete()

        builder.randgen = True
        modifiers = builder._build_modifiers_repr()
        assert isinstance(modifiers, ModifiersRepresentation)
        assert not modifiers.casegen
        assert modifiers.randgen
        assert modifiers.randgen_name == "name"
        assert modifiers.randgen_percent == 50

        choice = builder.create_concrete()
        assert isinstance(choice, Choice)
        assert not choice._leading_space
        assert len(choice._rules) == 0

class TestUnitRefBuilder(object):
    def test_creation(self):
        builder = UnitRefBuilder()
        assert not builder.leading_space
        assert not builder.casegen
        assert not builder.randgen
        assert builder.randgen_name is None
        assert builder.randgen_percent == 50

    def test_create_concrete(self):
        builder = UnitRefBuilder()
        builder.identifier = "id"

        with pytest.raises(ValueError):
            builder.create_concrete()

        builder.type = UnitType.alias
        modifiers = builder._build_modifiers_repr()
        assert isinstance(modifiers, ModifiersRepresentation)
        assert not modifiers.casegen
        assert not modifiers.randgen
        assert modifiers.randgen_name is None
        assert modifiers.randgen_percent == 50

        unit_ref = builder.create_concrete()
        assert isinstance(unit_ref, UnitReference)
        assert not unit_ref._leading_space
        assert unit_ref._unit_type == UnitType.alias
        assert unit_ref._name == "id"
