# coding: utf-8
"""
Test module.
Tests the functionalities that are present in module
`chatette.modifiers.randgen`
"""

import pytest

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
            should_generate("randgen name", 50, False, mapping)
            assert "randgen name" in mapping
        for _ in range(5):
            mapping = {"name": True}
            assert should_generate("name", 50, False, mapping)
        for _ in range(5):
            mapping = {"name": False}
            assert not should_generate("name", 50, False, mapping)
        for _ in range(5):
            mapping = {"name": False}
            assert should_generate("name", 50, True, mapping)
    
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

        empty = Example()
        examples = [Example("test1"), Example("test2")]
        all_examples = make_all_possibilities(examples, empty, "randgen", True)
        for ex in all_examples:
            current_mapping = getattr(ex, RANDGEN_MAPPING_KEY, dict())
            if ex == empty:
                assert current_mapping["randgen"]
            else:
                assert not current_mapping["randgen"]
    
    def test_errors(self):
        empty = Example()
        examples = [Example("test1"), Example("test2")]
        setattr(examples[0], RANDGEN_MAPPING_KEY, {"name": False})

        with pytest.raises(KeyError):
            make_all_possibilities(examples, empty, "name")

        examples[0] = Example("test1")
        setattr(examples[1], RANDGEN_MAPPING_KEY, {"name": True})

        with pytest.raises(KeyError):
            make_all_possibilities(examples, empty, "name")

        setattr(empty, RANDGEN_MAPPING_KEY, {"name": True})

        with pytest.raises(KeyError):
            make_all_possibilities([], empty, "name")


class TestCanConcatExamples(object):
    def test_no_mapping(self):
        ex1 = Example("test1")
        ex2 = Example()
        assert can_concat_examples(ex1, ex2)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"randgen name": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)
    
    def test_mapping_compatible(self):
        ex1 = Example("test1")
        ex2 = Example("test2")

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": True})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": False})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": False})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"other": True})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"other": False})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": False})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": False, "name2": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": False, "name2": True})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": False, "name2": True})
        assert can_concat_examples(ex1, ex2)
        assert can_concat_examples(ex2, ex1)
    
    def test_mapping_incompatible(self):
        ex1 = Example("test1")
        ex2 = Example("test2")

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": True})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": False})
        assert not can_concat_examples(ex1, ex2)
        assert not can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": False})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": True})
        assert not can_concat_examples(ex1, ex2)
        assert not can_concat_examples(ex2, ex1)

        setattr(ex1, RANDGEN_MAPPING_KEY, {"name": True, "name1": True})
        setattr(ex2, RANDGEN_MAPPING_KEY, {"name": True, "name1": False})
        assert not can_concat_examples(ex1, ex2)
        assert not can_concat_examples(ex2, ex1)


class TestMergeRandgenMappings(object):
    def test_empty_mappings(self):
        ex1 = Example()
        ex2 = Example()
        assert merge_randgen_mappings(ex1, ex2) is None

        ex1 = Example("test1")
        ex2 = Example("test2")
        assert merge_randgen_mappings(ex1, ex2) is None

    def test_no_merge(self):
        ex1 = Example("test1")
        ex2 = Example("test2")

        mapping = {"name": True}
        setattr(ex1, RANDGEN_MAPPING_KEY, mapping)

        assert merge_randgen_mappings(ex1, ex2) == mapping

        ex1 = Example("test1")
        setattr(ex2, RANDGEN_MAPPING_KEY, mapping)

        assert merge_randgen_mappings(ex1, ex2) == mapping

    def test_merge(self):
        ex1 = Example("test1")
        ex2 = Example("test2")

        mapping1 = {"name": True, "other": False}
        setattr(ex1, RANDGEN_MAPPING_KEY, mapping1)
        mapping2 = {"other": False, "third": True}
        setattr(ex2, RANDGEN_MAPPING_KEY, mapping2)

        assert \
            merge_randgen_mappings(ex1, ex2) == \
                {"name": True, "other": False, "third": True}


class TestConcatExamplesRandgen(object):
    def test_empty(self):
        ex1 = Example()
        ex2 = Example()
        assert concat_examples_with_randgen(ex1, ex2) == Example()

    def test_single(self):
        ex1 = Example("test1")
        ex2 = Example()
        mapping = {"name": True}
        setattr(ex1, RANDGEN_MAPPING_KEY, mapping)

        concated = concat_examples_with_randgen(ex1, ex2)
        assert concated.text == ex1.text
        assert getattr(concated, RANDGEN_MAPPING_KEY, None) == mapping
    
    def test_concat(self):
        ex1 = Example("test1")
        ex2 = Example("test2")
        mapping1 = {"name": True}
        mapping2 = {"other": False}
        setattr(ex1, RANDGEN_MAPPING_KEY, mapping1)
        setattr(ex2, RANDGEN_MAPPING_KEY, mapping2)

        concated = concat_examples_with_randgen(ex1, ex2)
        assert concated.text == "test1test2"
        assert \
            getattr(concated, RANDGEN_MAPPING_KEY, None) == \
                {"name": True, "other": False}
