# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.casegen`
"""

from chatette.modifiers.casegen import *
from chatette.units import Example


class TestModifyNbPossibilities(object):
    def test_modify_nb_possibilities(self):
        assert modify_nb_possibilities(0) == 0
        assert modify_nb_possibilities(1) == 2
        assert modify_nb_possibilities(100) == 200


class TestModifyExample(object):
    def test_modify_example(self):
        example = Example("text")
        for _ in range(5):
            modify_example(example)
            assert example.text in ("text", "Text")
        
        example = Example("  \talinea")
        for _ in range(5):
            modify_example(example)
            assert example.text in ("  \talinea", "  \tAlinea")


class TestMakeAllPossibilities(object):
    def test_make_all_pssibilities(self):
        examples = [Example("test"), Example(" alinea")]
        for ex in make_all_possibilities(examples):
            assert ex.text in ("test", "Test", " alinea", " Alinea")


class TestMayChangeLeadingCase(object):
    def test_empty(self):
        assert not may_change_leading_case("")
    
    def test_other(self):
        assert not may_change_leading_case("  ")
        assert not may_change_leading_case("\t ")
        assert not may_change_leading_case("123")
        assert may_change_leading_case("test")
        assert may_change_leading_case("\ttest")
        assert may_change_leading_case("TEST")


class TestWithLeadingUpper(object):
    def test_empty(self):
        example = Example()
        example = with_leading_upper(example)
        assert example.text == ""
    
    def test_other(self):
        example = Example("test")
        example = with_leading_upper(example)
        assert example.text == "Test"

        example = Example(" \talinea")
        example = with_leading_upper(example)
        assert example.text == " \tAlinea"


class TestWithLeadingLower(object):
    def test_empty(self):
        example = Example()
        example = with_leading_lower(example)
        assert example.text == ""
    
    def test_other(self):
        example = Example("test")
        example = with_leading_lower(example)
        assert example.text == "test"

        example = Example(" \talinea")
        example = with_leading_lower(example)
        assert example.text == " \talinea"
