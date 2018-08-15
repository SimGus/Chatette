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


class Parser():
    """
    This class will parse the input file(s)
    and create an internal representation of its contents.
    """

    COMMENT_SYM = ';'

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

        self.aliases = []  # for each alias, stores a list of list of units
        self.slots = []  # for each slot, stores a list of value name and unit
        self.intents = []  # for each intent, stores a list of list of slots


    def read_line(self):
        self.line_nb += 1
        return self.in_file.readline()

    def peek_line(self):
        """Returns the next line without moving forward in the file"""
        saved_pos = self.in_file.tell()
        line = self.in_file.readline()
        self.in_file.seek(saved_pos)
        return line


    def get_line_type(self, line, stripped_line):
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

    def is_inside_decl(self):
        next_line = self.peek_line()
        return (next_line.startswith(' ') or next_line.startswith('\t'))

    def parse(self):
        line = None
        while line != "":
            line = self.read_line()
            stripped_line = line.lstrip()
            line_type = self.get_line_type(line, stripped_line)

            if line_type == LineType.empty or line_type == LineType.comment:
                continue
            elif line_type == LineType.alias_declaration:
                self.parse_alias_definition(line)
            elif line_type == LineType.slot_declaration:
                self.parse_slot_definition(line)
            else:  # intent declaration
                self.parse_intent_definition(line)


    def check_indentation(self, indentation_nb, line, stripped_line):
        """
        Checks the indentation of the line is correct (raises a `SyntaxError`
        otherwise) and returns the number of spaces its indented with.
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

    def parse_alias_definition(self, first_line):
        """
        Parses the definition of an alias (declaration and contents)
        and adds the relevant info to the list of aliases.
        """
        printDBG("alias: "+first_line.strip())
        #
        (alias_name, alias_precision) = self.parse_alias_declaration(first_line)
        printDBG("name: "+alias_name+" precision: "+str(alias_precision))

        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = self.check_indentation(indentation_nb, line, stripped_line)

    def parse_alias_declaration(self, declaration):
        """
        Parses the declaration of an alias (the first line) and
        returns the alias name and its precision.
        """
        name = None
        precision = None
        decl_found = False
        for match in Parser.pattern_modifiers.finditer(declaration):
            match = match.groupdict()
            # printDBG("matched:"+str(match))
            if decl_found:
                raise SyntaxError("More than one declaration per line",
                    (self.in_file.name, self.line_nb, match.start(), line))
            else:
                decl_found = True

            name = match["name"]
            precision = match["precision"]
            if name == "":
                raise SyntaxError("Aliases must have a name (e.g. [name])",
                    (self.in_file.name, self.line_nb, match.start(), line))
            if precision == "":
                raise SyntaxError("Precision modifiers must have a name (e.g. [name#precision])",
                    (self.in_file.name, self.line_nb, match.start(), line))
            if match["randgen"] == "" or match["percentgen"] == "":
                raise SyntaxError("Alias declarations cannot have a random generation modifier",
                    (self.in_file.name, self.line_nb, match.start(), line))

        return (name, precision)


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
            indentation_nb = self.check_indentation(indentation_nb, line, stripped_line)

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
            indentation_nb = self.check_indentation(indentation_nb, line, stripped_line)


if __name__ == "__main__":
    import warnings
    warnings.warn("You are running the wrong file ('Parser.py')." +
        "The file that should be run is 'main.py'.")
