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
ANNOTATION_IGNORED_SYM = "'"

CHOICE_OPEN_SYM = r'{'
CHOICE_CLOSE_SYM = r'}'
CHOICE_SEP = '/'  # TODO: deprecate and rather use '|'

VARIATION_SYM = '#'
RAND_GEN_SYM = '?'  # This shouldn't be changed
PERCENT_GEN_SYM = '/'
CASE_GEN_SYM = '&'
ARG_SYM = '$'  # This shouldn't be changed

ALT_SLOT_VALUE_NAME_SYM = '='
ALT_SLOT_VALUE_FIRST_SYM = '/'

INCLUDE_FILE_SYM = '|'

# TODO add special characters at the beginning of those to prevent people from
#      using them by chance
RESERVED_VARIATION_NAMES = ["all-variations-aggregation", "rules",
                            "nb-gen-asked", "arg"]


PATTERN_COMMENT_DEPRECATED = re.compile(r"(?<!\\)" + COMMENT_SYM_DEPRECATED)
PATTERN_COMMENT = re.compile(r"(?<!\\)" + COMMENT_MARKER)

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

def remove_escapement(text):
    # pylint: disable=anomalous-backslash-in-string
    r"""
    Returns `text` were all escaped characters
    have been removed their escapement character (e.g. `\?` becomes `?`).
    Note that escaped dollar sign ($) are kept escaped until generation
    to avoid a possible bug with argument replacement.
    """
    if text is None:
        return None
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

# NOTE: there should be a most pretty way to deal with escapement
#       (especially when putting it back into strings).

def add_escapement_back_for_not_comments(text):
    """
    Considering that `text` contains no comment,
    escape comment markers and returns the new text.
    This function is needed because comment markers are several characters long.
    @pre: there is no comments anymore in `text`.
    """
    return text.replace(COMMENT_MARKER, ESCAPE_SYM+COMMENT_MARKER)
def add_escapement_back_in_sub_rule(text):
    """
    Put back escapement where it belongs for sub-rules
    (words and word groups) where escapement have been removed.
    """
    # BUG $ are always escaped
    escaped_text = ""
    for c in text:
        if should_be_escaped_char(c):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    return add_escapement_back_for_not_comments(escaped_text)
def add_escapement_back_in_word(text):
    """
    Put escapement back where it belongs in words
    where escapement has been removed.
    """
    escaped_text = ""
    for c in text:
        if c == ESCAPE_SYM or is_boundary_sym(c) or is_comment_sym(c):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    escaped_text = add_escapement_back_for_not_comments(escaped_text)
    return escaped_text.replace(ESCAPE_SYM+ESCAPE_SYM+ARG_SYM, ESCAPE_SYM+ARG_SYM)
def add_escapement_back_in_group(text):
    """
    Put escapement back where it belongs in word groups
    where escapement has been removed.
    """
    escaped_text = ""
    for c in text:
        if (   c == ESCAPE_SYM or is_boundary_sym(c)
            or is_group_modifier_sym(c) or is_comment_sym(c)):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    escaped_text = add_escapement_back_for_not_comments(escaped_text)
    return escaped_text.replace(ESCAPE_SYM+ESCAPE_SYM+ARG_SYM, ESCAPE_SYM+ARG_SYM)
def add_escapement_back_in_unit_ref(unit_name):
    """
    Put back escapement where it belongs for unit names in references
    where escapement have been removed.
    """
    escaped_text = ""
    for c in unit_name:
        if (   c == ESCAPE_SYM or is_boundary_sym(c) or is_comment_sym(c)
            or is_unit_ref_modifier_sym(c)):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    return add_escapement_back_for_not_comments(escaped_text)
def add_escapement_back_in_choice_item(text):
    """
    Put escapement back where it belongs in choice items
    where escapement has been removed.
    Add escapement only in items where escapement has already been added,
    not knowing they are part of a choice.
    """
    escaped_text = ""
    escaped = False
    for c in text:
        if escaped:
            escaped_text += c
            escaped = False
            continue
        if c == ESCAPE_SYM:
            escaped_text += c
            escaped = True
            continue
        if is_choice_special_sym(c):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    return escaped_text
def add_escapement_back_in_unit_decl(unit_name):
    """
    Put back escapement where it belongs for unit names in declarations
    where escapement have been removed.
    NOTE: not used at the moment
    """
    escaped_text = ""
    for c in unit_name:
        print(c)
        if (   c == ESCAPE_SYM or is_boundary_sym(c)
            or is_unit_decl_modifier_sym(c) or is_arg_sym(c) or is_comment_sym(c)):
            escaped_text += ESCAPE_SYM + c
        else:
            escaped_text += c
    return add_escapement_back_for_not_comments(escaped_text)


def should_be_escaped_char(text):
    """
    Returns `True` if `text` is 1 character that must be escaped in order to be
    considered part of a word.
    """
    return is_special_sym(text) or text == COMMENT_MARKER \
                                or text == COMMENT_SYM_DEPRECATED \
                                or text == ALT_SLOT_VALUE_NAME_SYM

def is_special_sym(text):
    """Returns `True` if `text` is a string made of only 1 special character."""
    return text == ALIAS_SYM or text == SLOT_SYM or text == INTENT_SYM or \
           text == UNIT_OPEN_SYM or text == UNIT_CLOSE_SYM or \
           text == VARIATION_SYM or text == RAND_GEN_SYM or \
           text == PERCENT_GEN_SYM or text == CASE_GEN_SYM or \
           text == ARG_SYM or text == CHOICE_OPEN_SYM or \
           text == CHOICE_CLOSE_SYM
def is_comment_sym(text):
    """Returns `True` iff `text` is a symbol introducing a comment."""
    return text in (COMMENT_MARKER, COMMENT_SYM_DEPRECATED)
def is_boundary_sym(text):
    """
    Returns `True` iff `text` is a symbol
    that makes the boundaries of special sub-rules.
    """
    return text in (ALIAS_SYM, SLOT_SYM, INTENT_SYM, UNIT_OPEN_SYM,
                    UNIT_CLOSE_SYM, CHOICE_OPEN_SYM, CHOICE_CLOSE_SYM)
def is_arg_sym(text):
    """Returns `True` iff `text` is the special symbol introducing arguments."""
    return text == ARG_SYM
def is_group_modifier_sym(text):
    """
    Returns `True` iff `text` is a special symbol introducing a modifier that
    can label word groups.
    """
    return text in (CASE_GEN_SYM, RAND_GEN_SYM, PERCENT_GEN_SYM)
def is_unit_ref_modifier_sym(text):
    """
    Returns `True` iff ´text´ is a special symbol introducing a modifier that
    can label unit references.
    """
    return text in (CASE_GEN_SYM, RAND_GEN_SYM, PERCENT_GEN_SYM, VARIATION_SYM,
                    ARG_SYM)
def is_unit_decl_modifier_sym(text):
    """
    Returns `True` iff `text` is a special symbol introducing a modifier that
    can label unit declarations.
    """
    return text in (CASE_GEN_SYM, VARIATION_SYM, ARG_SYM)
def is_choice_special_sym(text):
    """
    Returns `True` iff `text` is a special symbol in a choice (and in nothing
    else). This doesn't take into account boundary symbols.
    """
    return text == CHOICE_SEP

def is_unit_type_sym(text):
    """Returns `True` if `text` is a unit special symbol (`~`, `@` or `%`)."""
    return text == ALIAS_SYM or text == SLOT_SYM or text == INTENT_SYM

def is_start_unit_sym(char):
    """Checks if character `char` is the starting character of a special unit."""
    return char == UNIT_OPEN_SYM or char == ALIAS_SYM or \
           char == SLOT_SYM or char == INTENT_SYM


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
    if end_index == starting_index:
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
    end_index -= 1
    if end_index == starting_index:
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

    # TODO remove the following because you should allow ? and / in declarations?
    #      or the tokenizer should not consider them special characters in this
    #      case
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
    casegen_count = tokens_unit_inside.count(CASE_GEN_SYM)
    if casegen_count > 1:
        raise SyntaxError("There can be only one case generation modifier "+
                          "in a unit reference.")
    if casegen_count == 1 and tokens_unit_inside.index(CASE_GEN_SYM) != 0:
        raise SyntaxError("Case generation modifiers have to be at the start "+
                          "of a unit reference.")

    if casegen_count == 0 and is_special_sym(tokens_unit_inside[0]):
        raise SyntaxError("Unit references must be named.")
    elif casegen_count == 1 and len(tokens_unit_inside) <= 1:
        raise SyntaxError("Unit references must be named.")
    elif casegen_count == 1 and is_special_sym(tokens_unit_inside[1]):
        raise SyntaxError("Unit references must be named.")

    variation_count = tokens_unit_inside.count(VARIATION_SYM)
    if variation_count > 1:
        raise SyntaxError("There can be only one variation modifier "+
                          "in a unit reference.")
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
                          "per unit reference.")
    # if argument_count == 1:
    #     argument_name_index = tokens_unit_inside.index(ARG_SYM)+1
    #     if     argument_name_index >= len(tokens_unit_inside) \
    #         or is_special_sym(tokens_unit_inside[argument_name_index]):
    #         raise SyntaxError("Arguments must be named.")

    randgen_count = tokens_unit_inside.count(RAND_GEN_SYM)
    if randgen_count > 1:
        raise SyntaxError("There can be only one random generation modifier "+
                          "per unit reference.")
    percentgen_count = tokens_unit_inside.count(PERCENT_GEN_SYM)
    if percentgen_count > 1:
        raise SyntaxError("There can be only one percentage for generation "+
                          "modifier per unit reference.")
    if percentgen_count == 1 and randgen_count == 0:
        raise SyntaxError("There cannot be a percentage for generation "+
                          "modifier if there is no random generation modifier "+
                          "(did you mean to escape '"+PERCENT_GEN_SYM+"'?)")
    if percentgen_count == 1:
        index_randgen = tokens_unit_inside.index(RAND_GEN_SYM)
        index_percentgen = tokens_unit_inside.index(PERCENT_GEN_SYM)
        if index_randgen > index_percentgen:
            raise SyntaxError("A percentage for generation modifier must "+
                              "always be right after the random generation "+
                              "modifier.")
        if index_percentgen == len(tokens_unit_inside)-1:
            raise SyntaxError("No percentage found after the special symbol "+
                              "for percentage modifier.")
        try:
            percentgen = int(tokens_unit_inside[index_percentgen+1])
        except ValueError:
            raise SyntaxError("Percentage for generation modifiers need to be "+
                              "an integer.")
        if percentgen < 0 or percentgen > 100:
            raise SyntaxError("Percentage for generation modifiers need to be "+
                              "between 0 and 100.")

def check_choice_validity(tokens_choice_inside):
    """
    Check that the interior of a choice is syntactically legal.
    Deals with word groups as well.
    Raises a `SyntaxError` if the choice is invalid.
    As any sub-rules can be inside choices, we cannot check anything except
    that the last tokens is not a separator (or the two-to-last one if the
    last one is a random generation modifier).
    """
    # TODO: deprecate `/` as choice separators AND percentgen
    # percentgen_count = tokens_choice_inside.count(PERCENT_GEN_SYM)
    # if percentgen_count > 0:
    #     raise SyntaxError("Choices cannot take a percentage for generation "+
    #                       "modifier.")
    if len(tokens_choice_inside) > 0:
        if tokens_choice_inside[-1] == CHOICE_SEP:
            raise SyntaxError("Choice cannot end with a choice separator. " +
                              "Did you forget to escape the last character?")
        if (    len(tokens_choice_inside) > 1
            and tokens_choice_inside[-1] == RAND_GEN_SYM
            and tokens_choice_inside[-2] == CHOICE_SEP):
            raise SyntaxError("Choice ends with an empty choice item. " +
                              "Did you forget to escape the choice separator?")


def check_word_group_validity(tokens_word_group_inside):
    """
    Check that the interior of a choice is syntactically legal.
    Deals with word groups as well.
    Raises a `SyntaxError` if the choice is invalid.
    The constraints checked are:
    - there is only one modifier of each type
    - `/` and `#` are not there
    - `&` is at the beginning of the declaration (or nowhere)
    - choices are separated by '/' (not checked as there can be 0 or 1 choice)
    """
    casegen_count = tokens_word_group_inside.count(CASE_GEN_SYM)
    if casegen_count > 1:
        raise SyntaxError("There can be only one case generation modifier "+
                          "in a word group.")
    if casegen_count == 1 and tokens_word_group_inside.index(CASE_GEN_SYM) != 0:
        raise SyntaxError("Case generation modifiers have to be at the start "+
                          "of a word group.")

    variation_count = tokens_word_group_inside.count(VARIATION_SYM)
    if variation_count > 0:
        raise SyntaxError("Word groups cannot take variation modifiers.")

    argument_count = tokens_word_group_inside.count(ARG_SYM)
    if argument_count > 0:
        raise SyntaxError("Word groups cannot take arguments.")

    randgen_count = tokens_word_group_inside.count(RAND_GEN_SYM)
    if randgen_count > 1:
        raise SyntaxError("There can be only one random generation modifier "+
                          "per word group.")
    percentgen_count = tokens_word_group_inside.count(PERCENT_GEN_SYM)
    if percentgen_count > 1:
        raise SyntaxError("There can be only one percentage for generation "+
                          "modifier per word group.")
    if percentgen_count == 1 and randgen_count == 0:
        raise SyntaxError("There cannot be a percentage for generation "+
                          "modifier if there is no random generation modifier "+
                          "(did you mean to escape '"+PERCENT_GEN_SYM+"'?)")
    if percentgen_count == 1:
        index_randgen = tokens_word_group_inside.index(RAND_GEN_SYM)
        index_percentgen = tokens_word_group_inside.index(PERCENT_GEN_SYM)
        if index_randgen > index_percentgen:
            raise SyntaxError("A percentage for generation modifier must "+
                              "always be right after the random generation "+
                              "modifier.")
        if index_percentgen == len(tokens_word_group_inside)-1:
            raise SyntaxError("No percentage found after the special symbol "+
                              "for percentage modifier.")
        try:
            percentgen = int(tokens_word_group_inside[index_percentgen+1])
        except ValueError:
            raise SyntaxError("Percentage for generation modifiers need to be "+
                              "an integer.")
        if percentgen < 0 or percentgen > 100:
            raise SyntaxError("Percentage for generation modifiers need to be "+
                              "between 0 and 100.")


def find_name(tokens_inside_unit):
    """
    Finds the name of the unit from the tokens that represent the interior of
    a unit declaration or reference (inside the brackets (excluded)).
    @pre: there is no syntax error in this part.
    """
    start_index = 0
    if tokens_inside_unit[0] == CASE_GEN_SYM:
        start_index = 1
    name = ""
    while (   start_index < len(tokens_inside_unit)
          and not is_special_sym(tokens_inside_unit[start_index])):
        name += tokens_inside_unit[start_index]
        start_index += 1
    return remove_escapement(name)

def find_words(tokens_inside_word_group):
    """
    Finds the words in the tokens that represent the interior of a word group.
    Returns the list of those words in sequence.
    @pre: there is no syntax error in this part.
    """
    words = []
    for token in tokens_inside_word_group:
        if token == CASE_GEN_SYM:
            continue
        if  token in (RAND_GEN_SYM, VARIATION_SYM, ARG_SYM):
            return words
        words.append(token)
    return words


def find_modifiers_decl(tokens_inside_decl):
    """
    Finds and create a representation of the modifiers from a list of tokens
    representing the inside of a unit declaration. Returns the representation.
    If the percentage of generation was present but couldn't be
    @pre: there is no syntax error in this part (except possibly for
          percentage of generation).
    """
    modifiers = mods.UnitDeclarationModifiersRepr()

    i = 0
    if tokens_inside_decl[0] == CASE_GEN_SYM:
        modifiers.casegen = True
        i += 1

    expecting_variation = False
    expecting_argument = False
    while i < len(tokens_inside_decl):
        if tokens_inside_decl[i] == VARIATION_SYM:
            modifiers.variation_name = ""
            expecting_variation = True
            expecting_argument = False
        elif tokens_inside_decl[i] == ARG_SYM:
            modifiers.argument_name = ""
            expecting_variation = False
            expecting_argument = True
        elif expecting_variation:
            modifiers.variation_name += tokens_inside_decl[i]
        elif expecting_argument:
            modifiers.argument_name += tokens_inside_decl[i]
        i += 1

    modifiers.variation_name = remove_escapement(modifiers.variation_name)
    modifiers.argument_name = remove_escapement(modifiers.argument_name)

    return modifiers

def find_modifiers_reference(tokens_inside_reference):
    """
    Finds and create a representation of the modifiers from a list of tokens
    representing the inside of a reference. Returns the representation.
    @pre: there is no syntax error in this part.
    """
    modifiers = mods.ReferenceModifiersRepr()

    i = 0
    if tokens_inside_reference[0] == CASE_GEN_SYM:
        modifiers.casegen = True
        i += 1

    expecting_randgen_name = False
    expecting_percentgen = False
    expecting_variation = False
    expecting_argument = False
    while i < len(tokens_inside_reference):
        if tokens_inside_reference[i] == RAND_GEN_SYM:
            modifiers.randgen_name = ""
            expecting_randgen_name = True
            expecting_percentgen = False
            expecting_variation = False
            expecting_argument = False
        elif tokens_inside_reference[i] == PERCENT_GEN_SYM:
            expecting_randgen_name = False
            expecting_percentgen = True
            expecting_variation = False
            expecting_argument = False
        elif tokens_inside_reference[i] == VARIATION_SYM:
            modifiers.variation_name = ""
            expecting_randgen_name = False
            expecting_percentgen = False
            expecting_variation = True
            expecting_argument = False
        elif tokens_inside_reference[i] == ARG_SYM:
            modifiers.argument_value = ""
            expecting_randgen_name = False
            expecting_percentgen = False
            expecting_variation = False
            expecting_argument = True
        elif expecting_randgen_name:
            modifiers.randgen_name += tokens_inside_reference[i]
        elif expecting_percentgen:
            modifiers.percentage_randgen = int(tokens_inside_reference[i])
            expecting_percentgen = False
        elif expecting_variation:
            modifiers.variation_name += tokens_inside_reference[i]
        elif expecting_argument:
            modifiers.argument_value += tokens_inside_reference[i]
        i += 1

    modifiers.randgen_name = remove_escapement(modifiers.randgen_name)
    modifiers.variation_name = remove_escapement(modifiers.variation_name)
    modifiers.argument_value = remove_escapement(modifiers.argument_value)

    return modifiers

def find_modifiers_word_group(tokens_inside_word_group):
    """
    Finds and create a representation of the modifiers from a list of tokens
    representing the inside of a word group. Returns the representation.
    @pre: there is no syntax error in this part.
    """
    modifiers = mods.WordGroupModifiersRepr()

    i = 0
    if tokens_inside_word_group[0] == CASE_GEN_SYM:
        modifiers.casegen = True
        i += 1

    expecting_randgen_name = False
    expecting_percentgen = False
    while i < len(tokens_inside_word_group):
        if tokens_inside_word_group[i] == RAND_GEN_SYM:
            modifiers.randgen_name = ""
            expecting_randgen_name = True
            expecting_percentgen = False
        elif tokens_inside_word_group[i] == PERCENT_GEN_SYM:
            expecting_percentgen = True
            expecting_randgen_name = False
        elif expecting_randgen_name:
            modifiers.randgen_name += tokens_inside_word_group[i]
        elif expecting_percentgen:
            modifiers.percentage_randgen = int(tokens_inside_word_group[i])
            expecting_percentgen = False
        i += 1

    modifiers.randgen_name = remove_escapement(modifiers.randgen_name)

    return modifiers

def find_modifiers_choice(tokens_inside_choice):
    """
    Finds and create a representation of the modifiers from a list of tokens
    representing the inside of a choice. Returns the representation.
    @pre: there is no syntax error in this part.
    """
    modifiers = mods.ChoiceModifiersRepr()

    if tokens_inside_choice[0] == CASE_GEN_SYM:
        modifiers.casegen = True
    if tokens_inside_choice[-1] == RAND_GEN_SYM:
        modifiers.randgen = True

    return modifiers


def find_nb_examples_asked(annotation_interior):
    """
    Returns the training and testing number of examples asked for an intent
    declaration as a tuple. Returns `None` if the numbers given are not numbers.
    @pre: there is no syntax error in the annotation.
    """
    if len(annotation_interior) == 0:
        return None
    nb_train = None
    nb_test = None

    if len(annotation_interior) == 1:
        nb_train = annotation_interior[0]
    else:
        expecting_train = False
        expecting_test = False
        for token in annotation_interior:
            if (    token not in (ANNOTATION_ASSIGNMENT_SYM, ANNOTATION_SEP)
                and not token.isspace()):
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

    if nb_train is None and nb_test is None:
        return None

    if nb_train is not None:
        nb_train = nb_train.replace(ANNOTATION_IGNORED_SYM, "")
    if nb_test is not None:
        nb_test = nb_test.replace(ANNOTATION_IGNORED_SYM, "")

    try:
        nb_train = int(nb_train)
        if nb_test is None:
            nb_test = 0
        else:
            nb_test = int(nb_test)
    except ValueError:
        return None
    return (nb_train, nb_test)


def find_alt_slot_and_index(slot_rule_tokens):
    """
    Returns the index of the equal sign and the alt slot value as a 2-tuple,
    from the tokens representing a slot rule. Returns `None` if no alt slot
    value was found.
    @pre: there is no syntax error in this part.
    """
    try:
        index = slot_rule_tokens.index(ALT_SLOT_VALUE_NAME_SYM)
    except ValueError:
        return None
    if index+1 < len(slot_rule_tokens):
        i = index+1
        alt_slot_val = slot_rule_tokens[i]
        if alt_slot_val == ' ':
            alt_slot_val = ""
        i += 1
        while i < len(slot_rule_tokens):
            alt_slot_val += slot_rule_tokens[i]
            i += 1
        return (index, remove_escapement(alt_slot_val))
    return None


def next_choice_tokens(choice_interior_tokens):
    """
    Yields the next choice as a list of tokens in `choice_interior_tokens`.
    @pre: there is no syntax error in this part.
    """
    current_choice = []
    for (i, token) in enumerate(choice_interior_tokens):
        if token == CASE_GEN_SYM:
            continue
        elif token == RAND_GEN_SYM:
            if i == len(choice_interior_tokens)-1:  # Random generation symbol
                # NOTE: this should be changed if named randgen or percentgen
                #       is supported in the future.
                break
            else:  # Not a random generation symbol
                current_choice.append(token)
        elif token == CHOICE_SEP:
            yield current_choice
            current_choice = []
        else:
            current_choice.append(token)
    yield current_choice



def next_sub_rule_tokens(tokens):
    """
    Yields the next sub-rule from a rule
    represented as tokens (i.e. a list of str).
    @pre: `tokens` represents a valid rule.
    """
    current_sub_rule = []
    stop_with_char = None
    reading_sub_rule = False
    for token in tokens:
        if reading_sub_rule:
            if token == stop_with_char:
                current_sub_rule.append(token)
                yield current_sub_rule
                current_sub_rule = []
                stop_with_char = None
                reading_sub_rule = False
            else:
                current_sub_rule.append(token)
        else:  # Looking for the start of a sub-rule
            if is_start_unit_sym(token):  # Unit reference starting point
                current_sub_rule.append(token)
                reading_sub_rule = True
                stop_with_char = UNIT_CLOSE_SYM
            elif token == UNIT_OPEN_SYM:  # Word group starting point
                current_sub_rule.append(token)
                reading_sub_rule = True
                stop_with_char = UNIT_CLOSE_SYM
            elif token == CHOICE_OPEN_SYM:  # Word group starting point
                current_sub_rule.append(token)
                reading_sub_rule = True
                stop_with_char = CHOICE_CLOSE_SYM
            else:  # Word
                yield [token]


def is_sub_rule_word(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens` represents a word.
    @pre: considers `sub_rule_tokens` is never a single space.
    """
    return len(sub_rule_tokens) == 1
def is_sub_rule_word_group(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens`
    represents a word group.
    @pre: considers `sub_rule_tokens` to be a valid sub-rule.
    """
    return sub_rule_tokens[0] == UNIT_OPEN_SYM
def is_sub_rule_choice(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens`
    represents a choice.
    @pre: considers `sub_rule_tokens` to be a valid sub-rule.
    """
    return sub_rule_tokens[0] == CHOICE_OPEN_SYM
def is_sub_rule_alias_ref(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens`
    represents an alias reference.
    @pre: considers `sub_rule_tokens` to be a valid sub-rule.
    """
    return sub_rule_tokens[0] == ALIAS_SYM
def is_sub_rule_slot_ref(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens`
    represents a slot reference.
    @pre: considers `sub_rule_tokens` to be a valid sub-rule.
    """
    return sub_rule_tokens[0] == SLOT_SYM
def is_sub_rule_intent_ref(sub_rule_tokens):
    """
    Returns `True` if the list of str `sub_rule_tokens`
    represents an intent reference.
    @pre: considers `sub_rule_tokens` to be a valid sub-rule.
    """
    return sub_rule_tokens[0] == INTENT_SYM
