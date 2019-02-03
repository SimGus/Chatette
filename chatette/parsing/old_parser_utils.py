"""
Module `chatette.parsing.old_parser_utils`
Contains the utility functions for the old parser.
"""

from enum import Enum
import re

from chatette import deprecations
import chatette.parsing.parser_utils as pu
from chatette.parsing.parser_utils import SubRuleType

ALIAS_SYM = pu.ALIAS_SYM
SLOT_SYM = pu.SLOT_SYM
INTENT_SYM = pu.INTENT_SYM
ESCAPE_SYM = pu.ESCAPE_SYM
CHOICE_OPEN_SYM = pu.CHOICE_OPEN_SYM
CHOICE_CLOSE_SYM = pu.CHOICE_CLOSE_SYM
UNIT_CLOSE_SYM = pu.UNIT_CLOSE_SYM
ARG_SYM = pu.ARG_SYM
RAND_GEN_SYM = pu.RAND_GEN_SYM
CASE_GEN_SYM = pu.CASE_GEN_SYM
ALT_SLOT_VALUE_NAME_SYM = pu.ALT_SLOT_VALUE_NAME_SYM

RESERVED_VARIATION_NAMES = pu.RESERVED_VARIATION_NAMES

# This regex finds patterns like this `[name#variation?randgen/percentgen]`
# with `variation`, `randgen` and `percentgen` optional
PATTERN_UNIT_NAME = \
    re.compile(
        r"\[(?P<casegen>" + pu.CASE_GEN_SYM + r")?" +
        r"(?P<name>(?:\\[\\" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM +
        r"?\$\[\]]|[^\\\[\]" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM +
        r"?\$\n]+)+)[^\]]*\]"
    )
PATTERN_RANDGEN = re.compile(
    r"(?<!\\)\?(?P<randgen>(?:\\[\\\[\]" + pu.VARIATION_SYM +
    pu.PERCENT_GEN_SYM + r"?\$]|[^\\\[\]" + pu.VARIATION_SYM +
    pu.PERCENT_GEN_SYM + r"?\$\n]+)*)" +
    r"(?:" + pu.PERCENT_GEN_SYM + r"(?P<percentgen>[0-9]+))?"
)
PATTERN_VARIATION = re.compile(
    r"(?<!\\)" + pu.VARIATION_SYM +
    r"(?P<var>(?:\\[\\\[\]" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM +
    r"?\$]|[^\\\[\]" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM +
    r"?\$\n]+)+)"
)
PATTERN_ARG = re.compile(
    r"(?<!\\)\$(?P<arg>(?:\\[\\\[\]" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM
    + r"?\$]|[^\\\[\]" + pu.VARIATION_SYM + pu.PERCENT_GEN_SYM +
    r"?\$\n]+)+)"
)

_NB_TRAINING_GEN_NAME = "train(ing)?"
_NB_TEST_GEN_NAME = "test(ing)?"
PATTERN_NB_EXAMPLES_ASKED = re.compile(r"\]\((?P<nbgen>[0-9]+)\)")
PATTERN_NB_TRAINING_EXAMPLES_ASKED = \
    re.compile(r"'?" + _NB_TRAINING_GEN_NAME + r"'?\s*:\s*'?(?P<nbgen>[0-9]+)'?")
PATTERN_NB_TEST_EXAMPLES_ASKED = \
    re.compile(r"'?" + _NB_TEST_GEN_NAME + r"'?\s*:\s*'?(?P<nbgen_test>[0-9]+)'?")


class LineType(Enum):
    """Enumeration of all possible types of lines in an input file."""
    # UNUSED IN NEW PARSER
    empty = 1
    comment = 2
    alias_declaration = 3
    slot_declaration = 4
    intent_declaration = 5
    include_file = 6

class UnitType(Enum):
    """Enumeration of all possible types of unit declarations."""
    alias = 1
    slot = 2
    intent = 3


def strip_comments(text):
    """Returns the string `text` without the comments."""
    return pu.strip_comments(text)

def is_start_unit_sym(char):
    """Checks if character `char` is the starting character of a special unit."""
    return pu.is_start_unit_sym(char)

def remove_escapement(text):
    return pu.remove_escapement(text)


def get_top_level_line_type(line, stripped_line):
    """
    Returns the type of a top-level line (Note: this is expected to never
    be called for something else than a top-level line).
    Returns `None` if the top-level line is invalid.
    """
    if stripped_line == "":
        return LineType.empty
    elif stripped_line.startswith(pu.COMMENT_MARKER):
        return LineType.comment
    elif stripped_line.startswith(pu.COMMENT_SYM_DEPRECATED):
        deprecations.warn_semicolon_comments()
        return LineType.comment
    elif line.startswith(pu.ALIAS_SYM):
        return LineType.alias_declaration
    elif line.startswith(pu.SLOT_SYM):
        return LineType.slot_declaration
    elif line.startswith(pu.INTENT_SYM):
        return LineType.intent_declaration
    elif line.startswith(pu.INCLUDE_FILE_SYM):
        return LineType.include_file
    return None


def is_unit_start(text):
    """Checks if the string `text` is the start of a special unit."""
    return (len(text) > 0 and pu.is_start_unit_sym(text[0]))


def is_choice(text):
    """Checks if the string `text` is a choice."""
    return (len(text) > 0 and text.startswith(pu.CHOICE_OPEN_SYM))


def is_word(text):
    """Checks if the string `text` is a word alone (i.e. not a special unit)."""
    return not (len(text) <= 0 or text.isspace() or \
                text.startswith(pu.CHOICE_OPEN_SYM) or is_unit_start(text))


def get_unit_type(unit_text):
    """This function expects a string representing a unit"""
    if unit_text.startswith(pu.UNIT_OPEN_SYM):
        return pu.SubRuleType.word_group
    elif unit_text.startswith(pu.ALIAS_SYM):
        return pu.SubRuleType.alias
    elif unit_text.startswith(pu.SLOT_SYM):
        return pu.SubRuleType.slot
    elif unit_text.startswith(pu.INTENT_SYM):
        return pu.SubRuleType.intent
    elif unit_text.startswith(pu.CHOICE_OPEN_SYM):
        return pu.SubRuleType.choice
    else:
        raise RuntimeError("Internal error: tried to get the unit type of " +
                           "something that was not a unit: '" + unit_text + "'")


def find_nb_training_examples_asked(intent_text):
    """
    Finds the number of training examples asked for the provided intent string
    and returns it (or `None` if it wasn't provided).
    Raises a `ValueError` if the match is not an integer (shouldn't happen).
    """
    nb_training_examples_asked_str = None
    one_found = False
    patterns_list = [PATTERN_NB_EXAMPLES_ASKED,
                     PATTERN_NB_TRAINING_EXAMPLES_ASKED]
    for current_pattern in patterns_list:
        for match in current_pattern.finditer(intent_text):
            if one_found:
                raise SyntaxError("Expected only one number of training " +
                                  "examples asked in " + intent_text)
            else:
                one_found = True
            match = match.groupdict()

            nb_training_examples_asked_str = match["nbgen"]
    if nb_training_examples_asked_str is None:
        return None
    return int(nb_training_examples_asked_str)


def find_nb_testing_examples_asked(intent_text):
    """
    Finds the number of testing examples asked for the provided intent string
    and returns it (or `None` if it wasn't provided).
    Raises a `ValueError` if the match is not an integer (shouldn't happen).
    """
    nb_testing_examples_asked_str = None
    one_found = False
    for match in PATTERN_NB_TEST_EXAMPLES_ASKED.finditer(intent_text):
        if one_found:
            raise SyntaxError("Expected only one number of testing " +
                              "examples asked in '" + intent_text + "'")
        else:
            one_found = True
        match = match.groupdict()

        nb_testing_examples_asked_str = match["nbgen_test"]
    if nb_testing_examples_asked_str is None:
        return None
    return int(nb_testing_examples_asked_str)
