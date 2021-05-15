# coding: utf-8
"""
Test module.
Tests the functions and classes in module 'chatette.utils'.
"""

import sys
import imp
import pytest

import chatette.utils
from chatette.utils import \
    UnitType, Singleton, cast_to_unicode, sample_indulgent, rchop, str_to_bool, \
    remove_duplicates, min_if_exist, random_string, append_to_list_in_dict, \
    extend_list_in_dict


class TestUnitType(object):
    def test_existence(self):
        assert "UnitType" in dir(chatette.utils)
        assert "alias" in UnitType.__members__
        assert "slot" in UnitType.__members__
        assert "intent" in UnitType.__members__


class TestSingleton(object):
    def test_was_instantiated(self):
        assert not Singleton.was_instantiated()
        Singleton()
        assert Singleton.was_instantiated()

    def test_singleton(self):
        singleton = Singleton()
        other = Singleton()
        assert singleton == other
        third = Singleton.get_or_create()
        assert third == singleton

    def test_reset(self):
        singleton = Singleton()
        reset = Singleton.reset_instance()
        assert singleton != reset


class TestCastToUnicode(object):
    def test_nb(self):
        """Tests that the cast doesn't do anything for numeric types."""
        res_int = cast_to_unicode(5)
        assert res_int == 5

        res_float = cast_to_unicode(3.14159265)
        assert res_float == 3.14159265

        res_complex = cast_to_unicode(complex(1,2))
        assert res_complex == complex(1,2)

    def test_dict(self):
        dicts = [
            {"a": "b"}, {}, {"c": 0, 1: "d"}, {"e": {"f": "g", 0: ["h", 3]}}
        ]

        for d in dicts:
            res_dict = cast_to_unicode(d)
            if sys.version_info[0] == 3:
                assert res_dict == d
            else:
                self.check_is_unicode(res_dict)

    def check_is_unicode(self, anything):
        """This can only be called when running python 2.7."""
        if sys.version_info[0] != 2:
            pytest.fail(
                "Called unicode checker for python 2.7 " + \
                "using another python version."
            )
        if isinstance(anything, unicode):
            return True
        elif isinstance(anything, str):
            return False
        elif isinstance(anything, list):
            okay = True
            for e in anything:
                okay = okay and self.check_is_unicode(e)
                if not okay:
                    return False
            return okay
        elif isinstance(anything, dict):
            okay = True
            for key in anything:
                okay = okay and self.check_is_unicode(key) \
                            and self.check_is_unicode(anything[key])
                if not okay:
                    return False
            return okay
        return True


class TestSampleIndulgent(object):
    def test_sample(self):
        array = [2, 3, 5, 7, 11, 13]
        assert sample_indulgent(array, 1)[0] in array
        for item in sample_indulgent(array, 4):
            assert item in array
        for item in sample_indulgent(array, 1000):
            assert item in array

    def test_empty(self):
        assert len(sample_indulgent([], 5)) == 0


class TestRChop(object):
    def test_ending(self):
        assert rchop("this is a test", "test") == "this is a "
        assert rchop("another example", "ample") == "another ex"

    def test_not_ending(self):
        assert rchop("this is a test", "nothing") == "this is a test"
        assert rchop("Hello", "hello") == "Hello"


class TestStrToBool(object):
    def test_str_to_bool(self):
        assert str_to_bool("True") == True
        assert str_to_bool("False") == False
        assert str_to_bool("true") == True
        assert str_to_bool("false") == False
        assert str_to_bool("TRUE") == True
        assert str_to_bool("FALSE") == False
        assert str_to_bool("tRuE") == True
        assert str_to_bool("FaLSe") == False

    def test_not_bool(self):
        with pytest.raises(ValueError):
            str_to_bool("Test")


class TestRemoveDuplicates(object):
    def test_no_dup(self):
        dictionary = remove_duplicates({"a": ["one", "two"]})
        assert "a" in dictionary
        assert "one" in dictionary["a"]
        assert "two" in dictionary["a"]

    def test_dup(self):
        dictionary = remove_duplicates({"a": [1, 1], "b": ["o"]})
        assert "a" in dictionary
        assert "b" in dictionary
        assert 1 in dictionary["a"]
        assert "o" in dictionary["b"]
        assert len(dictionary["a"]) == 1


class TestMinIfExist(object):
    def test_min_if_exist(self):
        assert min_if_exist(None, None) is None
        assert min_if_exist(1, None) == 1
        assert min_if_exist(None, 0) == 0
        assert min_if_exist(5, 3) == 3
        assert min_if_exist(1.2, 8.12) == 1.2
        assert min_if_exist(-0.2, -8.9) == -8.9


class TestRandomString(object):
    def test_random_string(self):
        for i in range(12):
            assert len(random_string(12)) == 12


class TestAppendToListInDict(object):
    def test_append(self):
        dictionary = {"a": ["one"]}
        append_to_list_in_dict(dictionary, "b", 1)
        assert "b" in dictionary
        assert len(dictionary["b"]) == 1
        append_to_list_in_dict(dictionary, "a", 1)
        assert "a" in dictionary
        assert len(dictionary["a"]) == 2


class TestExtendListInDict(object):
    def test_extend(self):
        dictionary = {"a": ["one"], "b": [1,2]}
        extend_list_in_dict(dictionary, "c", [1,2])
        assert "c" in dictionary
        assert len(dictionary["c"]) == 2
        extend_list_in_dict(dictionary, "a", ["a", "bc"])
        assert "a" in dictionary
        assert len(dictionary["a"]) == 3


class TestMain(object):
    def test_main(self):
        imp.load_source("__main__", "chatette/utils.py")
