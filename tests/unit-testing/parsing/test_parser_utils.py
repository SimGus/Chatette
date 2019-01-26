"""
Test module.
Tests the functions in module 'chatette.parsing.parser_utils'.
"""

import pytest

from chatette.parsing.parser_utils import *


class TestStripComments(object):
    def test_empty(self):
        assert strip_comments("") == ""

    def test_no_comment(self):
        strings = ["test", "%[intent]", "@[slot]\t", "~[alias]", "\t{}test"]
        for s in strings:
            assert strip_comments(s) == s.rstrip()

    def test_only_old_comments(self):
        strings = ["; comment", ";", "\t;", ";this is a comment",
                   "\t ;a comment", ";a comment ; still a comment"]
        for s in strings:
            assert strip_comments(s) == ""
    
    def test_old_comments(self):
        s = "%[intent] ; comment"
        assert strip_comments(s) == "%[intent]"
        s = "@[slot]\t;comment"
        assert strip_comments(s) == "@[slot]"
        s = "~[alias];comment"
        assert strip_comments(s) == "~[alias]"
        s = "other ;\tcomment"
        assert strip_comments(s) == "other"

    def test_old_comments_escaped(self):
        s = r"test \; not a comment"
        assert strip_comments(s) == s
        s = r"\;"+"not a comment\t;comment"
        assert strip_comments(s) == "\;not a comment"
        s = "\ttest"+r"\; no comment; comment"
        assert strip_comments(s) == "\ttest"+r"\; no comment"
    
    def test_only_new_comments(self):
        strings = ["// comment", "//", "\t//", "//this is a comment",
                   "\t //a comment", "//a comment // still a comment"]
        for s in strings:
            assert strip_comments(s) == ""
    
    def test_new_comments(self):
        s = "%[intent] // comment"
        assert strip_comments(s) == "%[intent]"
        s = "@[slot]\t//comment"
        assert strip_comments(s) == "@[slot]"
        s = "~[alias]//comment"
        assert strip_comments(s) == "~[alias]"
        s = "other //\tcomment"
        assert strip_comments(s) == "other"

    def test_new_comments_escaped(self):
        s = r"test \// not a comment"
        assert strip_comments(s) == s
        s = r"\/\/"+"not a comment\t//comment"
        assert strip_comments(s) == "\/\/not a comment"
        s = "\ttest"+r"\// no comment// comment"
        assert strip_comments(s) == "\ttest"+r"\// no comment"

    def test_old_and_new_comments(self):
        s = "test // new comment ; old comment"
        assert strip_comments(s) == "test"
        s = "test ; old comment // new comment"
        assert strip_comments(s) == "test"


class TestRemoveEscapement(object):
    def test_empty(self):
        assert remove_escapement("") == ""

    def test_no_escapement(self):
        strings = ["word", "several different words",
                   "sentence with a [word group].", "%[intent](1) // comment",
                   "sentence with ~[alias?/90] ans @[slot]!", "{choice/too}"]
        for s in strings:
            assert remove_escapement(s) == s
    
    def test_single_escaped_special_symbols(self):
        assert remove_escapement("\?") == "?"
        assert remove_escapement("\;") == ";"
        assert remove_escapement("\/") == "/"
        assert remove_escapement("\//") == "//"
        assert remove_escapement("\/\/") == "//"
        assert remove_escapement("\[") == "["
        assert remove_escapement("\]") == "]"
        assert remove_escapement("\{") == "{"
        assert remove_escapement("\}") == "}"
        assert remove_escapement("\~") == "~"
        assert remove_escapement("\@") == "@"
        assert remove_escapement("\%") == "%"
        assert remove_escapement("\#") == "#"
        assert remove_escapement("\&") == "&"
        assert remove_escapement("\|") == "|"
        assert remove_escapement("\=") == "="
        
        assert remove_escapement("\$") == "\$"

    def test_several_words_escaped(self):
        s = r"test\? with several \? escapements\|"
        assert remove_escapement(s) == "test? with several ? escapements|"
        s = r"\[another [test\?] with] escapement\$2"
        assert remove_escapement(s) == "[another [test?] with] escapement\$2"


class TestIsSpecialSym(object):
    def test_empty(self):
        assert not is_special_sym(None)
        assert not is_special_sym("")
    
    def test_long_text(self):
        assert not is_special_sym("text")
        assert not is_special_sym("/Another test/")
    
    def test_not_special_char(self):
        symbols = ['a', ' ', '\t', '!']
        for sym in symbols:
            assert not is_special_sym(sym)
    
    def test_special_char(self):
        symbols = ['~', '@', '%', '[', ']', '#', '?', '/', '&', '$']
        for sym in symbols:
            assert is_special_sym(sym)


class TestIsUnitTypeSym(object):
    def test_empty(self):
        assert not is_unit_type_sym("")
    
    def test_long_text(self):
        assert not is_unit_type_sym("text")
        assert not is_unit_type_sym("~long test")
    
    def test_not_special_char(self):
        symbols = ['a', ' ', '\\', '!', '?']
        for sym in symbols:
            assert not is_unit_type_sym(sym)
    
    def test_special_char(self):
        symbols = ['~', '@', '%']
        for sym in symbols:
            assert is_unit_type_sym(sym)


class TestIsStartUnitSym(object):
    def test_not_unit_start_sym(self):
        symbols = ['', ' ', '\t', 'a', '0', '/', ';', '|', '{', ']', '}',
                   '(', ')']
        for sym in symbols:
            assert not is_start_unit_sym(sym)

    def test_not_char(self):
        objects = ["word", 0, False, str, ['a', '['], {1: 0}, None]
        for o in objects:
            assert not is_start_unit_sym(o)

    def test_unit_start_sym(self):
        unit_open_sym = '['
        assert is_start_unit_sym(unit_open_sym)
        alias_sym = '~'
        assert is_start_unit_sym(alias_sym)
        slot_sym = '@'
        assert is_start_unit_sym(slot_sym)
        intent_sym = '%'
        assert is_start_unit_sym(intent_sym)
    
    def test_unit_start_word(self):
        words = ["[unit]", "~[alias]", "@[slot]", "%[intent]"]
        for w in words:
            assert not is_start_unit_sym(w)


class TestGetUnitTypeFromSym(object):
    def test_empty(self):
        assert get_unit_type_from_sym("") is None
    
    def test_long_text(self):
        assert get_unit_type_from_sym("text") is None
        assert get_unit_type_from_sym("~long test") is None
    
    def test_not_unit_start_sym(self):
        symbols = ['a', ' ', '\t', '?', '#', '[', '}']
        for sym in symbols:
            assert get_unit_type_from_sym(sym) is None
    
    def test_special_sym(self):
        assert get_unit_type_from_sym('~') == UnitType.alias
        assert get_unit_type_from_sym('@') == UnitType.slot
        assert get_unit_type_from_sym('%') == UnitType.intent


class TestIsSubRuleWord(object):
    def test_empty(self):
        assert not is_sub_rule_word("")

    def test_not_words(self):
        tokens_list = [["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_word(tokens)
    
    def test_words(self):
        tokens_list = [["word"], ["other"], ["\?"]]
        for tokens in tokens_list:
            assert is_sub_rule_word(tokens)


class TestIsSubRuleWordGroup(object):
    def test_not_word_groups(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_word_group(tokens)
    
    def test_word_groups(self):
        tokens_list = [["[", "word", "]"], ["[", "word", "group", "]"],
                       ["[", "&", "word", "group", "\?", "?", "rand", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_word_group(tokens)


class TestIsSubRuleChoice(object):
    def test_not_choices(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"]]
        for tokens in tokens_list:
            assert not is_sub_rule_choice(tokens)

    def test_choices(self):
        tokens_list = [["{", "choice", "}"], ["{", "choice", "/", "2", "}"],
                       ["{", "choice", "word", "/", "[", "word", "group", "]", "}"],
                       ["{", "choice", "/", "choice", "?", "}"]]
        for tokens in tokens_list:
            assert is_sub_rule_choice(tokens)


class TestIsSubRuleAliasRef(object):
    def test_not_aliases(self):
        tokens_list = [["word"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_alias_ref(tokens)
    
    def test_aliases(self):
        tokens_list = [["~", "[", "alias", "]"], ["~", "[", "&", "a", "?", "]"],
                       ["~", "[", "alias", "?", "rand", "gen", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_alias_ref(tokens)


class TestIsSubRuleSlotRef(object):
    def test_not_slots(self):
        tokens_list = [["word"],
                       ["~", "[", "alias", "]"],
                       ["%", "[", "intent", "?", "rand", "]"],
                       ["[", "word", "group", "?", "]"],
                       ["{", "choice", "/", "2", "}"]]
        for tokens in tokens_list:
            assert not is_sub_rule_slot_ref(tokens)

    def test_slots(self):
        tokens_list = [["@", "[", "slot", "]"], ["@", "[", "s", "?", "r", "]"],
                       ["@", "[", "&", "slot", "?", "rand", "gen", "]"]]
        for tokens in tokens_list:
            assert is_sub_rule_slot_ref(tokens)
