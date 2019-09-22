# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.randgen`
"""


from chatette.modifiers.randgen import *
from chatette.units import Example

class TestModifyNbPossibilities(object):
    def test_modify_nb_possibilities(self):
        assert modify_nb_possibilities(0) == 1
        assert modify_nb_possibilities(1) == 2
        assert modify_nb_possibilities(10) == 11


class TestShouldGenerate(object):
    def test_should_generate(self):
        for _ in range(5):
            assert not should_generate(None, 0)
        for _ in range(5):
            assert should_generate(None, 100)
        
        for _ in range(5):
            mapping = dict()
            should_generate("randgen name", 50, mapping)
            assert "randgen name" in mapping
        for _ in range(5):
            mapping = {"name": True}
            assert should_generate("name", 50, mapping)
        for _ in range(5):
            mapping = {"name": False}
            assert not should_generate("name", 50, mapping)
    
class TestMakeAllPossibilities(object):
    def test_make_all_possibilities(self):
        empty = Example()
        examples = [Example("test1"), Example("test2")]
        all_examples = make_all_possibilities(examples, empty)
        assert empty in all_examples
        for ex in examples:
            assert ex in all_examples

        empty = Example()
        all_examples = make_all_possibilities(examples, empty, "randgen")
        for ex in all_examples:
            current_mapping = getattr(ex, RANDGEN_MAPPING_KEY, dict())
            if ex == empty:
                assert not current_mapping["randgen"]
            else:
                assert current_mapping["randgen"]


class TestCanConcatExamples(object):
    def test_no_mapping(self):
        ex1 = Example("test1")
        ex2 = Example()
        assert can_concat_examples(ex1, ex2)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"randgen name": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)
