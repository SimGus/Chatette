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
