# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.randgen`
"""


from chatette.modifiers.randgen import *

class TestModifyNbPossibilities(object):
    def test_modify_nb_possibilities(self):
        assert modify_nb_possibilities(0) == 1
        assert modify_nb_possibilities(1) == 2
        assert modify_nb_possibilities(10) == 11
