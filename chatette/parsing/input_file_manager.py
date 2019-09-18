# coding: utf-8
"""
Module `chatette.parsing.input_file_manager`
Contains the definition of the singleton `ÌnputFileManager`
which is in charge of managing the opening, closing and (read) accesses
to template files.
"""

import os.path

from chatette.utils import Singleton, cast_to_unicode
from chatette.parsing.line_count_file_wrapper import \
    LineCountFileWrapper
from chatette.statistics import Stats


class FileAlreadyOpened(ValueError):
    pass


class InputFileManager(Singleton):
    """
    Singleton in charge of managing the opening, closing and read accesses
    to templates file(s). In charge of raising the information about
    syntax errors if asked by other objects (namely the ones in charge of
    lexing and parsing the files).
    """
    _instance = None
    @classmethod
    def get_or_create(cls, file_path=None):
        """
        Returns the instance of the class (representing the singleton)
        or instantiate it if no instance already exists.
        If `file_path` is provided, starts to read it.
        """
        if cls._instance is None:
            cls._instance = cls(file_path)
        elif file_path is not None:
            cls._instance.open_file(file_path)
        return cls._instance
    
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
        `file_path` is understood with respect to the currently being parsed
        file (rather than working directory),
        unless it is an absolute path or there is no file currently being
        parsed.
        @raises: - `FileAlreadyOpened` if the file at `file_path`
                   was already opened.
        """
        file_path = cast_to_unicode(file_path)
        if not os.path.isabs(file_path):
            if self._current_file is None:
                file_path = cast_to_unicode(os.path.abspath(file_path))
            else:
                file_path = \
                    os.path.join(
                        cast_to_unicode(os.path.dirname(self._current_file.name)),
                        file_path
                    )

        opened_file_paths = [f.name for f in self._opened_files]
        if file_path in opened_file_paths:
            raise FileAlreadyOpened(
                "Tried to read file '" + file_path + "' several times."
            )

        if self._current_file is not None:
            self._opened_files.append(self._current_file)
        try:
            self._current_file = LineCountFileWrapper(file_path)
            Stats.get_or_create().new_file_parsed()
        except IOError as e:
            if len(self._opened_files) > 0:
                self._current_file = self._opened_files.pop()
            raise e
    
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
        if self._current_file is None:
            return (None, None)
        return (self._current_file.name, self._current_file.line_nb)
        
    def get_current_file_name(self):
        if self._current_file is None:
            return None
        return self._current_file.name

    def get_current_line_information(self):
        if self._current_file is None:
            return (None, None, self._last_read_line)
        return (
            self._current_file.name, self._current_file.line_nb,
            self._last_read_line
        )
    

    def syntax_error(self, message, char_index=0, word_to_find=None):
        """
        Closes all files and raises a `SyntaxError`
        pointing at the index `char_index` in the last read line.
        """
        if word_to_find is not None and line is not None:
            char_index = line.find(word_to_find)
        
        self.close_all_files()
        if self._current_file is not None:
            raise SyntaxError(  # BUG the file name and line read are sometimes not displayed (only the line number)
                message,
                (
                    self._current_file.name,
                    self._current_file.line_nb, char_index,
                    self._last_read_line
                )
            )
        raise SyntaxError(
            message,
            (None, None, char_index, self._last_read_line)
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
