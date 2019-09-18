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
