#!/usr/bin/env python3

from enum import Enum
import re

from utils import *

class Unit(Enum):
    word = 1  # simple word, no other info needed
    word_group = 2  # word group with modifiers
    alias = 3  # alias with modifiers
    slot = 4  # slot with modifiers
    intent = 5  # intent with modifiers and generation number

class LineType(Enum):
    empty = 1
    comment = 2
    alias_declaration = 3
    slot_declaration = 4
    intent_declaration = 5

def is_start_unit_sym(char):
    return (char == Parser.UNIT_OPEN_SYM or char == Parser.ALIAS_SYM or \
            char == Parser.SLOT_SYM or char == Parser.INTENT_SYM)
def is_unit(text):
    return (len(text) > 0 and is_start_unit_sym(text[0]))

def get_top_level_line_type(line, stripped_line):
    """
    Returns the type of a top-level line (Note: this is expected to never
    be called for something else than a top-level line).
    Raises an error if the top-level line is not valid
    """
    if stripped_line == "":
        return LineType.empty
    elif stripped_line.startswith(Parser.COMMENT_SYM):
        return LineType.comment
    elif line.startswith(Parser.ALIAS_SYM):
        return LineType.alias_declaration
    elif line.startswith(Parser.SLOT_SYM):
        return LineType.slot_declaration
    elif line.startswith(Parser.INTENT_SYM):
        return LineType.intent_declaration
    else:
        SyntaxError("Invalid syntax",
            (self.in_file.name, self.line_nb, 1, line))
def get_unit_type(unit):
    if unit.startswith(Parser.UNIT_OPEN_SYM):
        return Unit.word_group
    elif unit.startswith(Parser.ALIAS_SYM):
        return Unit.alias
    elif unit.startswith(Parser.SLOT_SYM):
        return Unit.slot
    elif unit.startswith(Parser.INTENT_SYM):
        return Unit.intent
    else:
        raise RuntimeError("Internal error: tried to get the unit type of "+
            "something that was not a unit")


def split_contents(text):
    """
    Splits `text` into a list of words and units
    (word groups, aliases, slots and intents).
    Keeps also track of units that have no space between them (this info is
    placed in the returned list).
    """
    words_and_units_raw = []
    current = ""
    escaped = False
    space_just_seen = False
    for c in text:
        # Manage character escapement
        if escaped:
            current += c
            escaped = False
            continue
        # Manage spaces
        if c.isspace():
            space_just_seen = True
            if current == "":
                continue
            elif not is_unit(current):
                # New word
                words_and_units_raw.append(current)
                current = ""
                continue
            else:
                current += c
                continue
        elif c == Parser.COMMENT_SYM:
            break
        elif c == Parser.ESCAPE_SYM:
            escaped = True
        # End unit
        elif c == Parser.UNIT_CLOSE_SYM:
            current += c
            words_and_units_raw.append(current)
            current = ""
        # New unit
        elif space_just_seen and current == "" and is_start_unit_sym(c):
            words_and_units_raw.append(' ')
            current += c
        # Any other character
        else:
            current += c

        if not c.isspace():
            space_just_seen = False

    # Make a list of unit from this parsing
    words_and_units = []
    for (i, string) in enumerate(words_and_units_raw):
        if string == ' ':
            continue
        elif not is_unit(string):
            words_and_units.append({
                "type": Unit.word,
                "word": string,
            })
        else:
            no_leading_space = i == 0 or (i != 0 and words_and_units_raw[i-1] != ' ')
            unit_type = get_unit_type(string)
            if unit_type == Unit.word_group:
                (name, precision, randgen, percentgen) = parse_unit(string)
                if precision is not None:
                    raise SyntaxError("Word groups cannot have a precision",
                        (self.in_file.name, self.line_nb, 0, string))
                words_and_units.append({
                    "type": Unit.word_group,
                    "words": name,
                    "randgen": randgen,
                    "percentgen": percentgen,
                    "leading-space": not no_leading_space,
                })
            else:
                (name, precision, randgen, percentgen) = parse_unit(string)
                words_and_units.append({
                    "type": unit_type,
                    "name": name,
                    "precision": precision,
                    "randgen": randgen,
                    "percentgen": percentgen,
                    "leading-space": not no_leading_space,
                })

    return words_and_units


def parse_unit(unit):
    """
    Parses a unit (left stripped) and returns
    (unit name, precision, randgen, percentgen) with `None` values for those
    not provided in the file.
    For a word group, the name will be its text.
    If an anonymous randgen is used '' will be its value.
    """
    # TODO case sensitivity leading &
    name = None
    precision = None
    randgen = None
    percentgen = None
    one_found = False
    for match in Parser.pattern_modifiers.finditer(unit):
        start_index = match.start()
        if one_found:  # this error would happen only when `unit` is a whole line (i.e. a declaration)
            raise SyntaxError("Expected only one unit here: only one declaration is allowed per line",
                (self.in_file.name, self.line_nb, start_index, unit))
        else:
            one_found = True
        match = match.groupdict()

        name = match["name"]
        precision = match["precision"]
        randgen = match["randgen"]
        percentgen = match["percentgen"]
        if name == "":
            raise SyntaxError("Units must have a name (or a content for word groups)",
                (self.in_file.name, self.line_nb, start_index, unit))
        if precision == "":
            raise SyntaxError("Precision must be named (e.g. [text#precision])",
                (self.in_file.name, self.line_nb, start_index, unit))
        if percentgen == "":
            raise SyntaxError("Percentage for generation cannot be empty",
                (self.in_file.name, self.line_nb, start_index, unit))

    return (name, precision, randgen, percentgen)


def check_indentation(indentation_nb, line, stripped_line):
    """
    Given the indentation of the previous line,
    checks the indentation of the line is correct (raises a `SyntaxError`
    otherwise) and returns the number of spaces its indented with.
    If this is the first line (`indentation_nb` is `None`),
    considers the indentation correct and returns the number of spaces
    the line is indented with.
    """
    current_indentation_nb = len(line) - len(stripped_line)
    if indentation_nb is None:
        return current_indentation_nb
    else:
        if current_indentation_nb == indentation_nb:
            return current_indentation_nb
        else:
            raise SyntaxError("Incorrect indentation",
                (self.in_file.name, self.line_nb, indentation_nb, line))



class Parser():  # TODO take out methods that manage only a couple of provided strings
    """
    This class will parse the input file(s)
    and create an internal representation of its contents.
    """

    COMMENT_SYM = ';'
    ESCAPE_SYM = '\\'

    ALIAS_SYM = '~'
    SLOT_SYM = '@'
    INTENT_SYM = '%'
    UNIT_OPEN_SYM = '['
    UNIT_CLOSE_SYM = ']'

    PRECISION_SYM = '#'

    # This regex finds patterns like this `[name#precision?randgen/percentgen]`
    # with `precision`, `randgen` and `percentgen` optional
    # TODO make this reflect the state of the symbols defined before
    pattern_modifiers = re.compile(r"\[(?P<name>[^#\[\]\?]*)(?:#(?P<precision>[^#\[\]\?]*))?(?:\?(?P<randgen>[^#\[\]\?/]*)(?:/(?P<percentgen>[^#\[\]\?]*))?)?\]")


    def __init__(self, input_file):
        self.in_file = input_file
        self.line_nb = 0

        self.aliases = dict()  # for each alias, stores a list of list of units
        self.slots = dict()  # for each slot, stores a list of value name and unit
        self.intents = dict()  # for each intent, stores a list of list of slots


    def read_line(self):
        self.line_nb += 1
        return self.in_file.readline()
    def peek_line(self):
        """Returns the next line without moving forward in the file"""
        saved_pos = self.in_file.tell()
        line = self.in_file.readline()
        self.in_file.seek(saved_pos)
        return line

    def is_inside_decl(self):
        next_line = self.peek_line()
        return (next_line.startswith(' ') or next_line.startswith('\t'))


    def parse(self):
        line = None
        while line != "":
            line = self.read_line()
            stripped_line = line.lstrip()
            line_type = get_top_level_line_type(line, stripped_line)

            if line_type == LineType.empty or line_type == LineType.comment:
                continue
            elif line_type == LineType.alias_declaration:
                self.parse_alias_definition(stripped_line)
            elif line_type == LineType.slot_declaration:
                self.parse_slot_definition(stripped_line)
            else:  # intent declaration
                self.parse_intent_definition(stripped_line)


    def parse_alias_definition(self, first_line):
        """
        Parses the definition of an alias (declaration and contents)
        and adds the relevant info to the list of aliases.
        """
        printDBG("alias: "+first_line.strip())
        # Manage the alias declaration
        (alias_name, alias_precision, randgen, percentgen) = \
            parse_unit(first_line)
        if randgen is not None:
            raise SyntaxError("Declarations cannot have a named random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))
        if percentgen is not None:
            raise SyntaxError("Declarations cannot have a random generation modifier",
                    (self.in_file.name, self.line_nb, 0, line))

        # Manage the contents
        expressions = []
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)

            expressions.append(split_contents(stripped_line))

        # Put the new definition in the alias dict
        if alias_name in self.aliases:
            if alias_precision is None:
                raise SyntaxError("Found a definition without precision for alias '"
                    +alias_name+"' while another definition was already found",
                    (self.in_file.name, self.line_nb, 0, first_line))
            else:
                self.aliases[alias_name].append({
                    "precision": alias_precision,
                    "expressions": expressions,
                })
        else:
            if alias_precision is None:
                self.aliases[alias_name] = {
                    "expressions": expressions,
                }
            else:
                self.aliases[alias_name] = [{
                    "precision": alias_precision,
                    "expressions": expressions,
                }]


    def parse_slot_definition(self, first_line):
        """
        Parses the definition of a slot (declaration and contents)
        and adds the relevant info to the list of slots.
        """
        printDBG("slot: "+first_line.strip())
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)


    def parse_intent_definition(self, first_line):
        """
        Parses the definition of an intent (declaration and contents)
        and adds the relevant info to the list of intents.
        """
        printDBG("intent: "+first_line.strip())
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = check_indentation(indentation_nb, line, stripped_line)


    def printDBG(self):
        print("\nAliases:")
        for name in self.aliases:
            current_alias_def = self.aliases[name]
            print("\t"+name+": ")
            if isinstance(current_alias_def, list):
                for precised_def in current_alias_def:
                    print("\t\tprecision: "+precised_def["precision"])
                    for expr in precised_def["expressions"]:
                        print("\t\t\texpression: "+str(expr))
            else:
                for expr in current_alias_def["expressions"]:
                    print("\t\texpression: "+str(expr))


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('Parser.py')." +
        "The file that should be run is 'main.py'.")
