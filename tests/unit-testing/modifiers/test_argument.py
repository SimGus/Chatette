# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.argument`
"""

from copy import deepcopy as clone

from chatette.modifiers.argument import *
from chatette.units import Example


class TestModifyNbPossibilities(object):
    def test_modify_nb_possibitilies(self):
        for i in range(10):
            assert i == modify_nb_possibilities(i)


class TestModifyExample(object):
    def test_no_mapping(self):
        example = Example()
        assert modify_example(clone(example), dict()) == example

        example = Example("test")
        assert modify_example(clone(example), dict()) == example

        example = Example("test with $ARG")
        assert modify_example(clone(example), dict()) == example

    def test_no_replacement(self):
        mapping = {"argument": "replaced"}

        example = Example()
        assert modify_example(clone(example), mapping) == example

        example = Example("test")
        assert modify_example(clone(example), mapping) == example

        example = Example("test with $ARG")
        assert modify_example(clone(example), mapping) == example

    def test_replacement(self):
        mapping = {"test": "TEST", "replace": "argument"}

        example = Example("replace $test by uppercase")
        modify_example(example, mapping)
        assert example.text == "replace TEST by uppercase"

        example = Example("is this $replace?")
        modify_example(example, mapping)
        assert example.text == "is this argument?"

        example = Example("The $replace is $test")
        modify_example(example, mapping)
        assert example.text == "The argument is TEST"


class TestMakeAllPossibilities(object):
    def test_no_mapping(self):
        examples = [Example(), Example("test1"), Example("$ARG")]

        for (original, modified) in zip(examples, make_all_possibilities(clone(examples), dict())):
            assert original == modified

    def test_no_replacement(self):
        mapping = {"argument": "replaced"}
        examples = [Example(), Example("test1"), Example("$ARG")]

        for (original, modified) in zip(examples, make_all_possibilities(clone(examples), mapping)):
            assert original == modified
