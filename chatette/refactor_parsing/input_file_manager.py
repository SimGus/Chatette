# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.input_file_manager`
Contains the definition of the singleton `ÌnputFileManager`
which is in charge of managing the opening, closing and (read) accesses
to template files.
"""

import os.path

from chatette.parsing.line_count_file_wrapper import LineCountFileWrapper


class InputFileManager(object):
    """
    Singleton in charge of managing the opening, closing and read accesses
    to templates file(s). In charge of raising the information about
    syntax errors if asked by other objects (namely the ones in charge of
    lexing and parsing the files).
    """
    instance = None

    @staticmethod
    def get_or_create(file_path=None):
        """
        Returns the instance of the class (representing the singleton)
        or instantiate it if no instance already exists.
        If `file_path` is provided, starts to read it.
        """
        if InputFileManager.instance is None:
            InputFileManager.instance = InputFileManager(file_path)
        elif file_path is not None:
            InputFileManager.instance.open_file(file_path)
        return InputFileManager.instance
    def reset_instance(file_path=None):
        """
        Completely resets the instance of the class (representing the singleton)
        ands makes a new one that opens the file at `file_path` if provided
        and returns this instance.
        """
        InputFileManager.instance = InputFileManager(file_path)
        return InputFileManager.instance
    
    def __init__(self, file_path=None):
        self._current_file = None
        self._opened_files = []

        self._last_read_line = None  # str

        if file_path is not None:
            self.open_file(file_path)
    
    def open_file(self, file_path):
        """
        Opens the file at `file_path` if and only if it wasn't opened before.
        Stores the currently read file for further reading if needed.
        @raises: - `ValueError` if the file at `file_path` was already opened.
        """
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        opened_file_paths = [f.name for f in self._opened_files]
        if file_path in opened_file_paths:
            raise ValueError(
                "Tried to read file '" + file_path + "' several times."
            )

        if self._current_file is not None:
            self._opened_files.append(self._current_file)
        self._current_file = LineCountFileWrapper(file_path)
    
    def close_all_files(self):
        """Closes all the opened files."""
        for f in self._opened_files:
            if not f.closed:
                f.close()
        if self._current_file is not None and not self._current_file.closed:
            self._current_file.close()
    def _close_current_file(self):
        """
        Closes current file and
        continues reading the file previously being read (if any).
        """
        if self._current_file is not None:
            self._current_file.close()
        if len(self._opened_files) > 0:
            self._current_file = self._opened_files.pop()
        else:
            self._current_file = None
    

    def get_current_file_information(self):
        return (self._current_file.name, self._current_file.line_nb)
    def get_current_filename(self):
        return self._current_file.name
    

    def syntax_error(self, message, char_index=0, word_to_find=None):
        """
        Closes all files and raises a `SyntaxError`
        pointing at the index `char_index` in the last read line.
        """
        if word_to_find is not None and line is not None:
            char_index = line.find(word_to_find)
        
        self.close_all_files()
        raise SyntaxError(
            message,
            (self._current_file.name, self._current_file.line_nb,
             char_index, self._last_read_line)
        )


    def read_line(self):
        """
        Reads the next line of `self._current_file` and
        returns it without the trailing new line (`\n`)
        (and any trailing whitespaces).
        If the file was entirely read, closes it and
        continues to read the file that was previously being read (if any).
        Returns `None` if there is no file left to read.
        """
        # TODO make this a generator?
        line = self._current_file.readline()
        while line == '':  # EOF
            self._close_current_file()
            if self._current_file is None:  # No more files to read
                return None
            line = self._current_file.readline()
        line = line.rstrip()
        self._last_read_line = line
        return line
