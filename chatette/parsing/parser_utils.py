#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.parsing.parser_utils`
Contains utility functions that are specific to
the parsing of template files.
"""


import re
from enum import Enum

from chatette import deprecations
import chatette.modifiers.representation as mods

COMMENT_SYM_DEPRECATED = ';'
COMMENT_MARKER = '//'
ESCAPE_SYM = '\\'

ALIAS_SYM = '~'
SLOT_SYM = '@'
INTENT_SYM = '%'
UNIT_OPEN_SYM = '['  # This shouldn't be changed
UNIT_CLOSE_SYM = ']'  # id.

ANNOTATION_OPEN_SYM = '('
ANNOTATION_CLOSE_SYM = ')'
ANNOTATION_SEP = ','
ANNOTATION_ASSIGNMENT_SYM = ':'

CHOICE_OPEN_SYM = r'{'
CHOICE_CLOSE_SYM = r'}'
CHOICE_SEP = '/'  # TODO: deprecate and rather use '|'

VARIATION_SYM = '#'
RAND_GEN_SYM = '?'  # This shouldn't be changed
PERCENT_GEN_SYM = '/'
CASE_GEN_SYM = '&'
ARG_SYM = '$'  # This shouldn't be changed

ALT_SLOT_VALUE_NAME_SYM = '='

INCLUDE_FILE_SYM = '|'

RESERVED_VARIATION_NAMES = ["all-variations-aggregation", "rules",
                            "nb-gen-asked", "arg"]

# This regex finds patterns like this `[name#variation?randgen/percentgen]`
# with `variation`, `randgen` and `percentgen` optional
PATTERN_UNIT_NAME = \
    re.compile(
        r"\[(?P<casegen>" + CASE_GEN_SYM + r")?" +
        r"(?P<name>(?:\\[\\" + VARIATION_SYM + PERCENT_GEN_SYM +
        r"?\$\[\]]|[^\\\[\]" + VARIATION_SYM + PERCENT_GEN_SYM +
        r"?\$\n]+)+)[^\]]*\]"
    )
PATTERN_RANDGEN = re.compile(
    r"(?<!\\)\?(?P<randgen>(?:\\[\\\[\]" + VARIATION_SYM +
    PERCENT_GEN_SYM + r"?\$]|[^\\\[\]" + VARIATION_SYM +
    PERCENT_GEN_SYM + r"?\$\n]+)*)" +
    r"(?:" + PERCENT_GEN_SYM + r"(?P<percentgen>[0-9]+))?"
)
PATTERN_VARIATION = re.compile(
    r"(?<!\\)" + VARIATION_SYM +
    r"(?P<var>(?:\\[\\\[\]" + VARIATION_SYM + PERCENT_GEN_SYM +
    r"?\$]|[^\\\[\]" + VARIATION_SYM + PERCENT_GEN_SYM +
    r"?\$\n]+)+)"
)
PATTERN_ARG = re.compile(
    r"(?<!\\)\$(?P<arg>(?:\\[\\\[\]" + VARIATION_SYM + PERCENT_GEN_SYM
    + r"?\$]|[^\\\[\]" + VARIATION_SYM + PERCENT_GEN_SYM +
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
PATTERN_COMMENT_DEPRECATED = re.compile(r"(?<!\\)" + COMMENT_SYM_DEPRECATED)
PATTERN_COMMENT = re.compile(r"(?<!\\)" + COMMENT_MARKER)

_NB_TRAINING_GEN_NAME = "train(ing)?"
_NB_TEST_GEN_NAME = "test(ing)?"
PATTERN_NB_EXAMPLES_ASKED = re.compile(r"\]\((?P<nbgen>[0-9]+)\)")
PATTERN_NB_TRAINING_EXAMPLES_ASKED = \
    re.compile(r"'?" + _NB_TRAINING_GEN_NAME + r"'?\s*:\s*'?(?P<nbgen>[0-9]+)'?")
PATTERN_NB_TEST_EXAMPLES_ASKED = \
    re.compile(r"'?" + _NB_TEST_GEN_NAME + r"'?\s*:\s*'?(?P<nbgen_test>[0-9]+)'?")

PATTERN_NB_TRAIN_EX_KEY = re.compile(r"'?train(ing)?'?")
PATTERN_NB_TEST_EX_KEY = re.compile(r"'?test(ing)?'?")


class UnitType(Enum):
    """Enumeration of all possible types of unit declarations."""
    alias = 1
    slot = 2
    intent = 3


class SubRuleType(Enum):  # TODO move this into unit defintions
    """
    Enumeration of all possible types of units.
    Note: word is not considered a 'special' unit (others are).
    """
    word = 1  # simple word, no other info needed
    word_group = 2  # word group with modifiers
    alias = 3  # alias with modifiers
    slot = 4  # slot with modifiers
    intent = 5  # intent with modifiers and generation number
    choice = 6  # choice with contained units


class LineType(Enum):
    """Enumeration of all possible types of lines in an input file."""
    empty = 1
    comment = 2
    alias_declaration = 3
    slot_declaration = 4
    intent_declaration = 5
    include_file = 6


def strip_comments(text):
    """Returns the text without the comments (and right stripped)."""
    if text is None:
        return None
    elif text == "":
        return ""
    match = PATTERN_COMMENT.search(text)
    match_deprecated = PATTERN_COMMENT_DEPRECATED.search(text)
    if match_deprecated is not None:
        deprecations.warn_semicolon_comments()

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


def is_special_sym(text):
    """Returns `True` if `text` is a string made of only 1 special character."""
    if text is None or len(text) != 1:
        return False
    return text == ALIAS_SYM or text == SLOT_SYM or text == INTENT_SYM or \
           text == UNIT_OPEN_SYM or text == UNIT_CLOSE_SYM or \
           text == VARIATION_SYM or text == RAND_GEN_SYM or \
           text == PERCENT_GEN_SYM or text == CASE_GEN_SYM or \
           text == CASE_GEN_SYM or text == ARG_SYM


def get_unit_type_from_sym(sym):
    """
    Returns which unit type corresponds to this special character.
    Returns `None` if it doesn't correspond to any unit type.
    """
    if sym == ALIAS_SYM:
        return UnitType.alias
    if sym == SLOT_SYM:
        return UnitType.slot
    if sym == INTENT_SYM:
        return UnitType.intent
    return None

def get_declaration_interior(tokens):
    """
    Returns a list of tokens that represent the inside of the declaration
    that is initiated on this line.
    Returns `None` if there is no unit declared in `tokens`.
    """
    length = len(tokens)
    starting_index = 0
    while starting_index < length and tokens[starting_index] != UNIT_OPEN_SYM:
        starting_index += 1
    starting_index += 1
    if starting_index >= length:
        print("s",starting_index,tokens)
        return None

    end_index = starting_index
    nb_closing_brackets_expected = 1
    while end_index < length and nb_closing_brackets_expected > 0:
        if tokens[end_index] == UNIT_OPEN_SYM:
            nb_closing_brackets_expected += 1
        elif tokens[end_index] == UNIT_CLOSE_SYM:
            nb_closing_brackets_expected -= 1
        end_index += 1
    end_index -= 1
    if end_index >= length:
        print("e:",end_index,tokens)
        return None

    return tokens[starting_index:end_index]

def get_annotation_interior(tokens):
    """
    Returns a list of tokens that represent the inside of the annotation
    that is present on this line.
    Returns `None` if there is no annotation in `tokens`.
    """
    length = len(tokens)
    starting_index = 0
    while starting_index < length and tokens[starting_index] != ANNOTATION_OPEN_SYM:
        starting_index += 1
    starting_index += 1
    if starting_index >= length:
        return None

    end_index = starting_index
    nb_closing_brackets_expected = 1
    while end_index < length and nb_closing_brackets_expected > 0:
        if tokens[end_index] == ANNOTATION_OPEN_SYM:
            nb_closing_brackets_expected += 1
        elif tokens[end_index] == ANNOTATION_CLOSE_SYM:
            nb_closing_brackets_expected -= 1
        end_index += 1
    if end_index >= length:
        return None

    return tokens[starting_index:end_index]


def check_declaration_validity(tokens_unit_inside):
    """
    Check that the interior of a declaration is syntactically legal.
    Raises a `SyntaxError` if the declaration is invalid.
    The constraints checked are:
    - there is only one modifier of each type
    - there are no randgen or percentgen modifiers
    - `&` is at the beginning of the declaration (or nowhere)
    - there is a name after `#`
    - there is a value after `$`
    - there is a name either after `&` or at the beginning
    - the variation names are not reserved
    """
    casegen_count = tokens_unit_inside.count(CASE_GEN_SYM)
    if casegen_count > 1:
        raise SyntaxError("There can be only one case generation modifier "+
                          "in a unit declaration.")
    if casegen_count == 1 and tokens_unit_inside.index(CASE_GEN_SYM) != 0:
        raise SyntaxError("Case generation modifiers have to be at the start "+
                          "of a unit declaration.")
    
    if casegen_count == 0 and is_special_sym(tokens_unit_inside[0]):
        print("a")
        raise SyntaxError("Unit declarations must be named.")
    elif casegen_count == 1 and len(tokens_unit_inside) <= 1:
        raise SyntaxError("Unit declarations must be named.")
    elif casegen_count == 1 and is_special_sym(tokens_unit_inside[1]):
        raise SyntaxError("Unit declarations must be named.")
    
    variation_count = tokens_unit_inside.count(VARIATION_SYM)
    if variation_count > 1:
        raise SyntaxError("There can be only one variation modifier "+
                          "in a unit declaration.")
    if variation_count == 1:
        variation_name_index = tokens_unit_inside.index(VARIATION_SYM)+1
        if     variation_name_index >= len(tokens_unit_inside) \
            or is_special_sym(tokens_unit_inside[variation_name_index]):
            raise SyntaxError("Variations must be named.")
        variation_name = tokens_unit_inside[variation_name_index]
        if variation_name in RESERVED_VARIATION_NAMES:
            raise SyntaxError("The following variation names are reserved: "+
                              str(RESERVED_VARIATION_NAMES)+". Please don't "+
                              "use them.")
    
    argument_count = tokens_unit_inside.count(ARG_SYM)
    if argument_count > 1:
        raise SyntaxError("There can be only one argument modifier "+
                          "per unit declaration.")
    if argument_count == 1:
        argument_name_index = tokens_unit_inside.index(ARG_SYM)+1
        if     argument_name_index >= len(tokens_unit_inside) \
            or is_special_sym(tokens_unit_inside[argument_name_index]):
            raise SyntaxError("Arguments must be named.")
    
    randgen_count = tokens_unit_inside.count(RAND_GEN_SYM)
    if randgen_count > 0:
        raise SyntaxError("Unit declarations cannot take a random generation "+
                          "modifier.")
    percentgen_count = tokens_unit_inside.count(PERCENT_GEN_SYM)
    if percentgen_count > 0:
        raise SyntaxError("Unit declarations cannot take a percentage for "+
                          "the random generation modifier.")


def check_reference_validity(tokens_unit_inside):
    """
    Check that the interior of a reference is syntactically legal.
    Raises a `SyntaxError` if the reference is invalid.
    The constraints checked are:
    - there is only one modifier of each type
    - `/` is not there unless `?` is there
    - there is a number between 0 and 100 if `/` is present
    - `&` is at the beginning of the declaration (or nowhere)
    - there is a name after `#`
    - there is a name either after `&` or at the beginning
    """
    pass # TODO


def find_name(tokens_inside_unit):
    """
    Finds the name of the unit from the tokens that represent the interior of
    a unit declaration or reference (inside the brackets (excluded)).
    @pre: there is no syntax error in this part.
    """
    if tokens_inside_unit[0] == CASE_GEN_SYM:
        return tokens_inside_unit[1]
    return tokens_inside_unit[0]

def find_modifiers_decl(tokens_inside_decl):
    """
    Finds and create a representation of the modifiers from a list of tokens
    representing the inside of a unit declaration. Returns the representation.
    @pre: there is no syntax error in this part.
    """
    modifiers = mods.UnitDeclarationModifiersRepr()

    i = 0
    if tokens_inside_decl[0] == CASE_GEN_SYM:
        modifiers.casegen = True
        i += 1
    
    expecting_randgen_name = False
    expecting_percentgen = False
    expecting_variation = False
    expecting_argument = False
    while i < len(tokens_inside_decl):
        if tokens_inside_decl[i] == VARIATION_SYM:
            expecting_variation = True
        elif tokens_inside_decl[i] == ARG_SYM:
            expecting_argument = True
            modifiers.argument_name = ""
        elif expecting_variation:
            modifiers.variation_name = tokens_inside_decl[i]
            expecting_variation = False
        elif expecting_argument:
            modifiers.argument_name = tokens_inside_decl[i]
            expecting_argument = False
        i += 1

    return modifiers


def find_nb_examples_asked(annotation_interior):
    """
    Returns the training and testing number of examples asked for an intent
    declaration as a tuple. Returns `None` if the numbers given are not numbers.
    @pre: there is no syntax error in the annotation.
    """
    nb_train = None
    nb_test = None

    expecting_train = False
    expecting_test = False
    for token in annotation_interior:
        if len(token) > 1:
            if PATTERN_NB_TRAIN_EX_KEY.match(token):
                expecting_train = True
            elif PATTERN_NB_TEST_EX_KEY.match(token):
                expecting_test = True
            elif expecting_train:
                nb_train = token
                expecting_train = False
            elif expecting_test:
                nb_test = token
                expecting_test = False
    
    try:
        nb_train = int(nb_train)
        if nb_test is None:
            nb_test = 0
        else:
            nb_test = int(nb_test)
    except ValueError:
        return None
    return (nb_train, nb_test)


def find_name_and_modifiers(tokens_unit_inside):
    """
    Finds the name and modifiers of the unit 
    from the tokens that represent the interior of
    a unit declaration or reference (inside the brackets).
    HACK: Returns the information as a dictionary.
    Returns `None` if nothing was found.
    """
    casegen = False
    randgen_name = None
    percentgen = None
    variation = None
    argument = None
    unit_name = None

    i = 0
    if tokens_unit_inside[0] == CASE_GEN_SYM:
        casegen = True
        i += 1
    
    expecting_randgen_name = False
    expecting_percentgen = False
    expecting_variation = False
    expecting_argument = False
    while i < len(tokens_unit_inside):
        if tokens_unit_inside[i] == RAND_GEN_SYM:
            expecting_randgen_name = True
            randgen_name = ""
        elif tokens_unit_inside[i] == PERCENT_GEN_SYM:
            expecting_percentgen = True
            percentgen = ""
        elif tokens_unit_inside[i] == VARIATION_SYM:
            expecting_variation = True
            variation = ""
        elif tokens_unit_inside[i] == ARG_SYM:
            expecting_argument = True
            argument = ""
        elif expecting_randgen_name:
            randgen_name = tokens_unit_inside[i]
            expecting_randgen_name = False
        elif expecting_percentgen:
            percentgen = tokens_unit_inside[i]
            expecting_percentgen = False
        elif expecting_variation:
            variation = tokens_unit_inside[i]
            expecting_variation = False
        elif expecting_argument:
            argument = tokens_unit_inside[i]
            expecting_argument = False
        else:
            unit_name = tokens_unit_inside[i]
        i += 1

    return {"name": unit_name, "casegen": casegen, "randgen": randgen_name,
            "percentgen": percentgen, "variation": variation,
            "argument": argument}


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
        deprecations.warn_semicolon_comments()
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
    """Checks if character `char` is the starting character of a special unit."""
    return (char == UNIT_OPEN_SYM or char == ALIAS_SYM or \
            char == SLOT_SYM or char == INTENT_SYM)


def is_unit_start(text):
    """Checks if the string `text` is the start of a special unit."""
    return (len(text) > 0 and is_start_unit_sym(text[0]))


def is_choice(text):
    """Checks if the string `text` is a choice."""
    return (len(text) > 0 and text.startswith(CHOICE_OPEN_SYM))


def is_word(text):
    """Checks if the string `text` is a word alone (i.e. not a special unit)."""
    return not (len(text) <= 0 or text.isspace() or \
                text.startswith(CHOICE_OPEN_SYM) or is_unit_start(text))


def get_unit_type(unit_text):
    """This function expects a string representing a unit"""
    if unit_text.startswith(UNIT_OPEN_SYM):
        return SubRuleType.word_group
    elif unit_text.startswith(ALIAS_SYM):
        return SubRuleType.alias
    elif unit_text.startswith(SLOT_SYM):
        return SubRuleType.slot
    elif unit_text.startswith(INTENT_SYM):
        return SubRuleType.intent
    elif unit_text.startswith(CHOICE_OPEN_SYM):
        return SubRuleType.choice
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


def remove_escapement(text):
    # pylint: disable=anomalous-backslash-in-string
    r"""
    Returns `text` were all escaped characters
    have been removed their escapement character (e.g. `\?` becomes `?`).
    Note that escaped dollar sign ($) are kept escaped until generation
    to avoid a possible bug with argument replacement.
    """
    if ESCAPE_SYM not in text:
        return text
    # Note there might be better ways to do this with regexes
    # (but they have fixed-length negative lookback)
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
