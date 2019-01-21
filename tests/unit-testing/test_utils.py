"""
Test module.
Tests the functions in module 'chatette.utils'.
"""

import sys
import pytest
import imp

import chatette.utils
from chatette.utils import cast_to_unicode, choose


class TestPrints(object):
    def test_existences(self):
        assert "print_DBG" in dir(chatette.utils)
        assert "print_warn" in dir(chatette.utils)
    
    def test_no_return(self):
        assert chatette.utils.print_DBG("Test") is None
        assert chatette.utils.print_warn("Test") is None


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
        dicts = [{"a": "b"}, {}, {"c": 0, 1: "d"}, {"e": {"f": "g", 0: ["h", 3]}}]

        for d in dicts:
            res_dict = cast_to_unicode(d)
            if sys.version_info[0] == 3:
                assert res_dict == d
            else:
                self.check_is_unicode(res_dict)

    def check_is_unicode(self, anything):
        """This can only be called when running python 2.7."""
        if sys.version_info[0] != 2:
            pytest.fail("Called unicode checker for python 2.7 "+
                        "using another python version.")
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


class TestChoose(object):
    def test_empty_array(self):
        assert choose([]) is None
    
    def test_not_array(self):
        with pytest.raises(TypeError, message="Expecting TypeError when calling"+
                                              "choose on None"):
            choose(None)
        with pytest.raises(TypeError, message="Expecting TypeError when calling"+
                                              "choose on an integer"):
            choose(5)
        with pytest.raises(TypeError, message="Expecting TypeError when calling"+
                                              "choose on a floating number"):
            choose(3.14)
        with pytest.raises(KeyError, message="Expecting TypeError when calling"+
                                              "choose on a dict"):
            choose({"a": 5})

    def test_short_array(self):
        arrays = [[1],[1,2,3],["a","b"],[None,4,2.7,int]]
        for array in arrays:
            res = choose(array)
            assert res in array

    def test_long_array(self):
        arrays = [
                    [1,2,3,4,5,6,7,8,9,10,11],
                    ["a","b","c","d","hello","pytest","very","long","array"],
                    [None,4,2.7,int,"different",["tests",1],{"a": 18, 0: None}]
                 ]
        for array in arrays:
            res = choose(array)
            assert res in array


class TestMain(object):
    def test_main(self):
        imp.load_source("__main__", "chatette/utils.py")
