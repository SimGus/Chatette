#!/usr/bin/env python3

from enum import Enum

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
                self.parse_alias(line)
            elif line_type == LineType.slot_declaration:
                self.parse_slot(line)
            else: # intent declaration
                self.parse_intent(line)


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

    def parse_alias(self, first_line):
        printDBG("alias: "+first_line.strip())
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = self.check_indentation(indentation_nb, line, stripped_line)

    def parse_slot(self, first_line):
        printDBG("slot: "+first_line.strip())
        indentation_nb = None
        while self.is_inside_decl():
            line = self.read_line()
            stripped_line = line.lstrip()
            indentation_nb = self.check_indentation(indentation_nb, line, stripped_line)

    def parse_intent(self, first_line):
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
