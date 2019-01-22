"""
Module `chatette.parsing.tokenizer`
Contains the tokenizer used by the parser.
"""

import io, os

from chatette.utils import print_warn
import chatette.parsing.parser_utils as pu
from chatette.parsing.line_count_file_wrapper import LineCountFileWrapper


class Tokenizer(object):
    def __init__(self, master_filename=None):  # TODO remove default values
        self.current_file = None
        self.opened_files = []
        if master_filename is not None:
            self.master_file_dir = os.path.dirname(master_filename)
            self.current_file = LineCountFileWrapper(master_filename)

    def open_file(self, filename):
        """
        Stores the current file for future use and opens `filename`.
        `filename` is given relatively to the master file.
        """
        if self.current_file is not None:
            self.opened_files.append(self.current_file)
        filepath = os.path.join(self.master_file_dir, filename)
        self.current_file = LineCountFileWrapper(filepath)

    def close_files(self):
        for f in self.opened_files:
            f.close()
        if self.current_file is not None and not self.current_file.closed:
            self.current_file.close()

    def close_current_file(self):
        if self.current_file is not None:
            self.current_file.close()
        if len(self.opened_files) > 0:
            self.current_file = self.opened_files.pop()
        else:
            self.current_file = None

    def get_file_information(self):
        return (self.current_file.name, self.current_file.line_nb)


    def read_line(self):
        """
        Reads a line of `self.current_file` and returns it without the trailing
        new line (`\n`).
        If the file was entirely read, closes it and continues to read the
        file that was previously being read (returning its next line).
        Returns `None` if there is no file left to read.
        """
        line = self.current_file.readline()
        while line == '':  # EOF
            self.close_current_file()
            if self.current_file is None:  # No more files to read
                return None
            else:
                line = self.current_file.readline()
        return line.rstrip()

    def next_tokenized_line(self):
        """
        Yields the next relevant line of the current file as a list of tokens.
        An irrelevant line is an empty or comment line.
        """
        while True:
            line_str = self.read_line()
            if line_str is None:
                break
            if pu.is_irrelevant_line(line_str):
                continue
            yield self.new_tokenize(line_str)


    def new_tokenize(self, text):
        """
        Returns a tokenized version of the string `text`,
        i.e. a list of strings that make up words or special characters.
        The string `~[alias?] word. [&group]` would be tokenized into
        `["~", "[", "alias", "?", "]", " ", "word.", "[", "&", "group", "]"]`.
        @pre: `text` is not `None` or ''.
        """
        return text.split()


    def tokenize(self, text, line_nb=None, in_file_name=None):
        """Splits a string in a list of tokens (as strings)"""
        tokens = []
        current = ""

        escaped = False
        inside_choice = False
        for c in text:
            # Manage escapement
            if escaped:
                current += c
                escaped = False
                continue
            # elif c == pu.COMMENT_SYM_DEPRECATED:
            #     break
            elif inside_choice:
                if c == pu.CHOICE_CLOSE_SYM:
                    tokens.append(current + c)
                    current = ""
                    inside_choice = False
                else:
                    current += c
            elif c == pu.ESCAPE_SYM:
                escaped = True
                current += c
            elif c.isspace():
                if not pu.is_unit_start(current) and not pu.is_choice(current):  # End of word
                    if current != "":
                        tokens.append(current)
                    tokens.append(' ')
                    current = ""
                elif current == "" and \
                        len(tokens) > 0 and tokens[-1] == ' ':
                    continue  # Double space in-between words
                else:
                    current += c
            elif c == pu.UNIT_CLOSE_SYM:
                if pu.is_unit_start(current):
                    tokens.append(current + c)
                    current = ""
                else:
                    print_warn("Inconsistent use of the unit close symbol (" +
                               pu.UNIT_CLOSE_SYM + ") at line " + str(line_nb) +
                               " of file '" + in_file_name +
                               "'. Consider escaping them if they are " +
                               "not supposed to close a unit.\nThe generation will " +
                               "however continue, considering it as a normal character.")
                    current += c
            elif c == pu.CHOICE_CLOSE_SYM:
                print_warn("Inconsistent use of the choice close symbol (" +
                           pu.CHOICE_CLOSE_SYM + ") at line " + str(line_nb) +
                           " of file '" + in_file_name +
                           "'. Consider escaping them if they are " +
                           "not supposed to close a unit.\nThe generation will " +
                           "however continue, considering it as a normal character.")
                current += c
            elif c == pu.CHOICE_OPEN_SYM:
                if current != "":
                    tokens.append(current)
                inside_choice = True
                current = c
            elif pu.is_start_unit_sym(c) and current != pu.ALIAS_SYM and \
                    current != pu.SLOT_SYM and current != pu.INTENT_SYM:
                if current != "":
                    tokens.append(current)
                current = c
            else:  # Any other character
                current += c
        if current != "":
            tokens.append(current)
        return tokens
