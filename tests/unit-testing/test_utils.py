"""
Test module.
Tests the functions in module 'chatette.utils'.
"""

import sys
import pytest
import imp

import chatette.utils
from chatette.utils import cast_to_unicode


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


class TestMain(object):
    def test_main(self):
        imp.load_source("__main__", "chatette/utils.py")
