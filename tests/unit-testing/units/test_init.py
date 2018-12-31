"""
Test module.
Tests the functions in module 'chatette.utils'.
"""

from chatette.units import Example, may_change_leading_case, \
                           randomly_change_case, with_leading_upper, \
                           with_leading_lower, may_get_leading_space


class TestExample(object):
    def test_repr(self):
        assert str(Example()) == "<'' []>"
        assert str(Example("test")) == "<'test' []>"
        assert str(Example("test", [1])) == "<'test' [1]>"


class TestMayChangeLeadingCase(object):
    def test_empty(self):
        assert not may_change_leading_case("")
    
    def test_may_not_change_case(self):
        strings = ["1", " 1", "\t!", "~[alias]", "\t(Why?)"]
        for s in strings:
            assert not may_change_leading_case(s)
    
    def test_may_change_case(self):
        strings = ["word", "\ttest", "CAPITAL", "\t Several words"]
        for s in strings:
            assert may_change_leading_case(s)


class TestRandomlyChangeCase(object)            :
    def test_empty(self):
        assert randomly_change_case("") == ""
    
    def test_no_change(self):
        strings = ["123", "\t\t", "!!!", "()", "{something else}"]
        for s in strings:
            assert randomly_change_case(s) == s

    def test_change(self):
        strings = ["test", "\tindentation", "Several words", "IN CAPITAL?"]
        lower_str = ["test", "\tindentation", "several words", "iN CAPITAL?"]
        upper_str = ["Test", "\tIndentation", "Several words", "IN CAPITAL?"]
        for (i,s) in enumerate(strings):
            assert randomly_change_case(s) in (lower_str[i], upper_str[i])


class TestWithLeadingUpper(object):
    def test_empty(self):
        assert with_leading_upper("") == ""

    def test_no_change(self):
        strings = ["12", "  ", "???", "(test)"]
        for s in strings:
            assert with_leading_upper(s) == s

    def test_change(self):
        strings = ["test", "\tindentation", "Several words", "IN CAPITAL?"]
        upper_str = ["Test", "\tIndentation", "Several words", "IN CAPITAL?"]
        for (i,s) in enumerate(strings):
            assert with_leading_upper(s) == upper_str[i]


class TestWithLeadingLower(object):
    def test_empty(self):
        assert with_leading_lower("") == ""

    def test_no_change(self):
        strings = ["12", "  ", "???", "(test)"]
        for s in strings:
            assert with_leading_lower(s) == s

    def test_change(self):
        strings = ["test", "\tindentation", "Several words", "IN CAPITAL?"]
        lower_str = ["test", "\tindentation", "several words", "iN CAPITAL?"]
        for (i,s) in enumerate(strings):
            assert with_leading_lower(s) == lower_str[i]


class TestMayGetLeadingSpace(object):
    def test_empty(self):
        assert not may_get_leading_space("")

    def test_may_not(self):
        strings = [" !", " 42", " \t(test)", "  ~[alias]", " // comment", "  "]
        for s in strings:
            assert not may_get_leading_space(s)

    def test_may(self):
        strings = ["word", "Capitalized", "several words", "UPPER CASE"]
        for s in strings:
            assert may_get_leading_space(s)
