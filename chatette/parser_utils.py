#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
import re

from chatette import deprecations
from chatette.utils import *
import chatette.deprecations

COMMENT_SYM_DEPRECATED = ';'
COMMENT_MARKER = '//'
ESCAPE_SYM = '\\'

ALIAS_SYM = '~'
SLOT_SYM = '@'
INTENT_SYM = '%'
UNIT_OPEN_SYM = '['  # This shouldn't be changed
UNIT_CLOSE_SYM = ']'  # id.

CHOICE_OPEN_SYM = r'{'
CHOICE_CLOSE_SYM = r'}'
CHOICE_SEP = '/'

VARIATION_SYM = '#'
RAND_GEN_SYM = '?'  # This shouldn't be changed
PERCENT_GEN_SYM = '/'
CASE_GEN_SYM = '&'
ARG_SYM = '$'  # This shouldn't be changed

ALT_SLOT_VALUE_NAME_SYM = '='

INCLUDE_FILE_SYM = '|'

RESERVED_VARIATION_NAMES = ["all-variations-aggregation", "rules", "nb-gen-asked", "arg"]

# This regex finds patterns like this `[name#variation?randgen/percentgen]`
# with `variation`, `randgen` and `percentgen` optional
pattern_unit_name = \
    re.compile(
        r"\[(?P<casegen>"+CASE_GEN_SYM+r")?"+
        r"(?P<name>(?:\\[\\"+VARIATION_SYM+PERCENT_GEN_SYM+
            r"?\$\[\]]|[^\\\[\]"+VARIATION_SYM+PERCENT_GEN_SYM+
            r"?\$\n]+)+)[^\]]*\]"
    )
pattern_randgen = re.compile(
                    r"(?<!\\)\?(?P<randgen>(?:\\[\\\[\]"+VARIATION_SYM+
                        PERCENT_GEN_SYM+r"?\$]|[^\\\[\]"+VARIATION_SYM+
                        PERCENT_GEN_SYM+r"?\$\n]+)*)"+
                    r"(?:"+PERCENT_GEN_SYM+r"(?P<percentgen>[0-9]+))?"
                  )
pattern_variation = re.compile(
                        r"(?<!\\)"+VARIATION_SYM+
                        r"(?P<var>(?:\\[\\\[\]"+VARIATION_SYM+PERCENT_GEN_SYM+
                            r"?\$]|[^\\\[\]"+VARIATION_SYM+PERCENT_GEN_SYM+
                            r"?\$\n]+)+)"
                    )
pattern_arg = re.compile(
                r"(?<!\\)\$(?P<arg>(?:\\[\\\[\]"+VARIATION_SYM+PERCENT_GEN_SYM
                    +r"?\$]|[^\\\[\]"+VARIATION_SYM+PERCENT_GEN_SYM+
                    r"?\$\n]+)+)"
              )
# TODO make this reflect the state of the symbols defined before
# pattern_modifiers = \
#     re.compile(
#         r"\[(?P<casegen>&)?"+
#         r"(?P<name>[^#\[\]\?/\$]*)"+
#         r"(?:\$(?P<arg>[^#\[\]?/\$]*))?"+
#         r"(?:#(?P<variation>[^#\[\]\?/\$]*))?"+
#         r"(?:\?(?P<randgen>[^#\[\]\?/\$]*)(?:/(?P<percentgen>[^#\[\]\?/\$]*))?)?\]"
#     )
pattern_comment_deprecated = re.compile(r"(?<!\\)"+COMMENT_SYM_DEPRECATED)
pattern_comment = re.compile(r"(?<!\\)"+COMMENT_MARKER)

_nb_training_gen_name = "training"
_nb_test_gen_name = "testing"
pattern_nb_examples_asked = re.compile(r"\]\((?P<nbgen>[0-9]+)\)")
pattern_nb_training_examples_asked = \
    re.compile(r"'"+_nb_training_gen_name+r"': '(?P<nbgen>[0-9]+)'")
pattern_nb_testing_examples_asked = \
    re.compile(r"'"+_nb_test_gen_name+r"': '(?P<nbgen_test>[0-9]+)'")


class Unit(Enum):  # TODO move this into unit defintions
    word = 1  # simple word, no other info needed
    word_group = 2  # word group with modifiers
    alias = 3  # alias with modifiers
    slot = 4  # slot with modifiers
    intent = 5  # intent with modifiers and generation number
    choice = 6  # choice with contained units

class LineType(Enum):
    empty = 1
    comment = 2
    alias_declaration = 3
    slot_declaration = 4
    intent_declaration = 5
    include_file = 6


def strip_comments(text):
    match = pattern_comment.search(text)
    match_deprecated = pattern_comment_deprecated.search(text)
    if match_deprecated is not None:
        deprecations.warn_deprecation_semicolon_comments()

    if match is None and match_deprecated is None:
        return text.rstrip()
    elif match_deprecated is None:
        return text[:match.start()].rstrip()
    elif match is None:
        return text[:match_deprecated.start()].rstrip()
    else:
        if match.start() <= match_deprecated.start():
            return text[:match.start()].rstrip()
        return text[:match_deprecated.start()].rstrip()

def get_top_level_line_type(line, stripped_line):
    """
    Returns the type of a top-level line (Note: this is expected to never
    be called for something else than a top-level line).
    Returns `None` if the top-level line is invalid.
    """
    if stripped_line == "":
        return LineType.empty
    elif stripped_line.startswith(COMMENT_MARKER):
        return LineType.comment
    elif stripped_line.startswith(COMMENT_SYM_DEPRECATED):
        deprecations.warn_deprecation_semicolon_comments()
        return LineType.comment
    elif line.startswith(ALIAS_SYM):
        return LineType.alias_declaration
    elif line.startswith(SLOT_SYM):
        return LineType.slot_declaration
    elif line.startswith(INTENT_SYM):
        return LineType.intent_declaration
    elif line.startswith(INCLUDE_FILE_SYM):
        return LineType.include_file
    return None

def is_start_unit_sym(char):
    return (char == UNIT_OPEN_SYM or char == ALIAS_SYM or \
            char == SLOT_SYM or char == INTENT_SYM)
def is_unit_start(text):
    return (len(text) > 0 and is_start_unit_sym(text[0]))
def is_choice(text):
    return (len(text) > 0 and text.startswith(CHOICE_OPEN_SYM))
def is_word(text):
    return not (text.startswith(CHOICE_OPEN_SYM) or is_unit_start(text))

def get_unit_type(unit_text):
    """This function expects a string representing a unit"""
    if unit_text.startswith(UNIT_OPEN_SYM):
        return Unit.word_group
    elif unit_text.startswith(ALIAS_SYM):
        return Unit.alias
    elif unit_text.startswith(SLOT_SYM):
        return Unit.slot
    elif unit_text.startswith(INTENT_SYM):
        return Unit.intent
    elif unit_text.startswith(CHOICE_OPEN_SYM):
        return Unit.choice
    else:
        raise RuntimeError("Internal error: tried to get the unit type of "+
            "something that was not a unit: '"+unit_text+"'")


def find_nb_training_examples_asked(intent_text):
    """
    Finds the number of training examples asked for the provided intent string
    and returns it (or `None` if it wasn't provided).
    """
    nb_training_examples_asked = None
    one_found = False
    patterns_list = [pattern_nb_examples_asked,
                     pattern_nb_training_examples_asked]
    for current_pattern in patterns_list:
        for match in current_pattern.finditer(intent_text):
            start_index = match.start()
            if one_found:
                raise SyntaxError("Expected only one number of training "+
                                  "examples asked in "+intent_text)
            else:
                one_found = True
            match = match.groupdict()

            nb_training_examples_asked = match["nbgen"]
    return nb_training_examples_asked
def find_nb_testing_examples_asked(intent_text):
    """
    Finds the number of testing examples asked for the provided intent string
    and returns it (or `None` if it wasn't provided).
    """
    nb_testing_examples_asked = None
    one_found = False
    for match in pattern_nb_testing_examples_asked.finditer(intent_text):
        start_index = match.start()
        if one_found:
            raise SyntaxError("Expected only one number of testing "+
                              "examples asked in '"+intent_text+"'")
        else:
            one_found = True
        match = match.groupdict()

        nb_testing_examples_asked = match["nbgen_test"]
    return nb_testing_examples_asked


def get_all_rules_in_variations(definition):
    """
    Returns a list of all the rules for all variations of `definition`
    which is a definition for an alias or a slot (nothing else).
    """
    all_rules = []
    if "rules" in definition:  # No variation
        all_rules.extend(definition["rules"])
    else:
        for variation in definition:
            if variation != "all-variations-aggregation":
                all_rules.extend(definition[variation]["rules"])  # TODO manage arg
    return all_rules

def get_all_rules_in_intent_variations(definition):
    """As `get_all_rules_in_variations` for intents"""
    # `definition` is a dict indexed by the names of the variation, each
    # containing a dict with the nb of generations to do for this intent
    # and the rules in `rules`
    all_rules = []
    for variation in definition:
        if variation != "all-variations-aggregation":
            all_rules.extend(definition[variation]["rules"])
    return all_rules


def remove_escapement(text):
    """
    Returns `text` were all escaped characters
    have been removed their escapement character
    """
    if ESCAPE_SYM not in text:
        return text
    # Note there might be better ways to do this with regexes (but they have fixed-length negative lookback)
    result = ""
    escaped = False
    for c in text:
        if escaped and c == ARG_SYM:  # Keep \$ until generation
            result += ESCAPE_SYM + ARG_SYM
            escaped = False
        elif escaped:
            result += c
            escaped = False
        elif c == ESCAPE_SYM:
            escaped = True
        else:
            result += c
    return result
