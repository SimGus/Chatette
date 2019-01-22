"""
Module `chatette.parsing.tokenizer`
Contains the tokenizer used by the parser.
"""

import io, os

from chatette.utils import print_warn, print_DBG
import chatette.parsing.parser_utils as pu
from chatette.parsing.line_count_file_wrapper import LineCountFileWrapper


class Tokenizer(object):
    def __init__(self, master_filename=None):  # TODO remove default values
        self.current_file = None
        self.opened_files = []
        if master_filename is not None:
            self.master_file_dir = os.path.dirname(master_filename)
            self.current_file = LineCountFileWrapper(master_filename)

        self._last_read_line = None

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
            if not f.closed:
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


    def fail(self, exception):
        """Closes all files before raising an exception."""
        self.close_files()
        raise exception
    def syntax_error(self, message, line=None, line_index=0):
        """Makes an exception to be raised after closing all files."""
        if line is None:
            line = self._last_read_line
        exception = SyntaxError(message, (self.current_file.name,
                                          self.current_file.line_nb,
                                          line_index, line))
        self.fail(exception)


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
            line = self.current_file.readline()
        line = line.rstrip()
        self._last_read_line = line
        return line

    def next_tokenized_line(self):
        """
        Yields the next relevant line of the current file as a list of tokens.
        An irrelevant line is an empty or comment line.
        """
        while True:
            line_str = pu.strip_comments(self.read_line())
            if line_str is None:
                break
            if line_str == "":
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
        tokens = []
        current_token = ""

        def store_current_token():
            if current_token != "":
                tokens.append(current_token)
            return ""

        indentation = Tokenizer._get_indentation(text)
        if indentation is not None:
            tokens.append(indentation)
            text = text.lstrip()

        if indentation is None and text[0] == pu.INCLUDE_FILE_SYM:
            return [pu.INCLUDE_FILE_SYM, text[1:]]
        
        nb_closing_brackets_expected = 0  # For unit declaration initiators and references
        expecting_percent_gen = False  # True in a sub-rule after a `?`
        after_unit_declaration = False
        inside_annotation = False  # For parentheses after declaration initiator
        inside_choice = False
        next_char_escaped = False

        for (i,c) in enumerate(text):
            # Escapement
            if next_char_escaped:
                current_token += c
                next_char_escaped = False
            elif c == pu.ESCAPE_SYM:
                next_char_escaped = True
            # Unit special characters
            elif c == pu.ALIAS_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif c == pu.SLOT_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif c == pu.INTENT_SYM:
                current_token = store_current_token()
                tokens.append(c)
            # Unit brackets
            elif c == pu.UNIT_OPEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
                nb_closing_brackets_expected += 1
            elif c == pu.UNIT_CLOSE_SYM:
                if nb_closing_brackets_expected < 1:
                    self.syntax_error("Inconsistent use of unit brackets "+
                                      "(too many closing unit symbols '"+
                                      pu.UNIT_CLOSE_SYM+"').", text, i)
                current_token = store_current_token()
                tokens.append(c)
                nb_closing_brackets_expected -= 1
                if indentation is None and nb_closing_brackets_expected == 0:
                    after_unit_declaration = True
            # Choice
            elif c == pu.CHOICE_OPEN_SYM:
                if inside_choice:
                    self.syntax_error("Nested choices are not supported. "+
                                      "Did you mean to escape it ('"+
                                      pu.ESCAPE_SYM+pu.CHOICE_OPEN_SYM+
                                      "' instead of '"+pu.CHOICE_OPEN_SYM+"'?",
                                      text, i)
                current_token = store_current_token()
                tokens.append(c)
                inside_choice = True
            elif c == pu.CHOICE_CLOSE_SYM:
                if not inside_choice:
                    self.syntax_error("Cannot close a choice before "+
                                      "opening it. Did you mean to escape "+
                                      "it ('"+pu.ESCAPE_SYM+
                                      pu.CHOICE_CLOSE_SYM+"' instead of '"+
                                      pu.CHOICE_CLOSE_SYM+"'?",
                                      text, i)
                current_token = store_current_token()
                tokens.append(c)
                inside_choice = False
            elif inside_choice and c == pu.CHOICE_SEP:
                current_token = store_current_token()
                tokens.append(c)
            # Inside unit
            elif nb_closing_brackets_expected > 0 and c == pu.VARIATION_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif nb_closing_brackets_expected > 0 and c == pu.RAND_GEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
                expecting_percent_gen = True
            elif nb_closing_brackets_expected > 0 and expecting_percent_gen and c == pu.PERCENT_GEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
                expecting_percent_gen = False
            elif nb_closing_brackets_expected > 0 and c == pu.CASE_GEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif nb_closing_brackets_expected > 0 and c == pu.ARG_SYM:
                current_token = store_current_token()
                tokens.append(c)
            # Inside choice
            elif inside_choice and c == pu.RAND_GEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif inside_choice and c == pu.CASE_GEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
            # Slot alternative value
            elif nb_closing_brackets_expected == 0 and c == pu.ALT_SLOT_VALUE_NAME_SYM:
                current_token = store_current_token()
                tokens.append(c)
            # Annotation
            elif after_unit_declaration and c == pu.ANNOTATION_OPEN_SYM:
                current_token = store_current_token()
                tokens.append(c)
                inside_annotation = True
                after_unit_declaration = False
            elif inside_annotation and c == pu.ANNOTATION_CLOSE_SYM:
                current_token = store_current_token()
                tokens.append(c)
                inside_annotation = False
            elif inside_annotation and c == pu.ANNOTATION_ASSIGNMENT_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif inside_annotation and c == pu.ANNOTATION_SEP:
                current_token = store_current_token()
                tokens.append(c)
            # Spaces
            elif c.isspace():
                if not current_token.isspace():
                    store_current_token()
                    current_token = c
            # Other
            else:
                if current_token.isspace() and not c.isspace():
                    current_token = store_current_token()
                current_token += c
                if after_unit_declaration:
                    after_unit_declaration = False
        store_current_token()

        if nb_closing_brackets_expected > 0:
            self.syntax_error("Line ends with open unit(s).", text, i)
        if inside_annotation:
            self.syntax_error("Line ends with an open annotation.", text, i)
        if inside_choice:
            self.syntax_error("Line ends with open choice(s).", text, i)
        if next_char_escaped:
            self.syntax_error("Line ends with unexpected escapement '"+
                              pu.ESCAPE_SYM+"'.", text, i)
        
        return tokens



    @staticmethod
    def _get_indentation(text):
        """
        Returns a string that is made
        of all the spaces at the beginning of `text`.
        """
        i = 0
        length = len(text)
        indentation = ""
        while i < length and text[i].isspace():
            indentation += text[i]
            i += 1
        if indentation != "":
            return indentation
        return None


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
