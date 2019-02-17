"""
Module `chatette.terminal_writer`.
Contains a wrapper of the output of commands, that can write to the terminal
(stdout) or to a file.
"""

from __future__ import print_function
import io
import os.path
from enum import Enum


class RedirectionType(Enum):  # QUESTION is it possible to merge this with relevant strings?
    truncate = 1
    append = 2
    quiet = 3


class TerminalWriter(object):
    """Wrapper of `print` that can write to stdout or to a file."""
    def __init__(self, redirection_type=RedirectionType.append,
                 redirection_file_path=None):
        self.redirection_file_path = redirection_file_path
        self.set_redirection_type(redirection_type)
        self.buffered_text = None

    def reset(self):
        self.redirection_file_path = None
        self.buffered_text = None
    def set_redirection_type(self, redirection_type):
        """
        Sets redirection type.
        @pre: `redirection_type` is of type `RedirectionType`.
        """
        if redirection_type is None:
            self._file_mode = None
            return
        if redirection_type == RedirectionType.append:
            self._file_mode = 'a+'
        elif redirection_type == RedirectionType.truncate:
            self._file_mode = 'w+'
        else:
            self._file_mode = 'quiet'

    def get_redirection(self):
        """
        Returns a 2-tuple containing the type and file path of the redirection.
        If this wrapper doesn't redirect to any file (or ignore prints),
        returns `None`.
        """
        if self._file_mode is None:
            return None
        if self._file_mode == 'quiet':
            return (RedirectionType.quiet, None)
        if self._file_mode == 'a+':
            return (RedirectionType.append, self.redirection_file_path)
        if self._file_mode == 'w+':
            return (RedirectionType.truncate, self.redirection_file_path)
        return None


    def write(self, text):
        if self.redirection_file_path is None and self._file_mode is None:
            print(text)
        elif self._file_mode == 'quiet':
            return
        else:
            if self.buffered_text is None:
                self.buffered_text = str(text)
            else:
                self.buffered_text +='\n' + str(text)

    def error_log(self, text):
        processed_text = ''.join(['\t' + line + '\n'
                                  for line in text.split('\n')])
        self.write("[ERROR]"+processed_text[:-1])


    def flush(self):
        """
        Flushes the buffered text to the redirection file
        if such a file is provided.
        """
        if self.redirection_file_path is not None:
            # Create file if it doesn't exist
            if not os.path.isfile(self.redirection_file_path):
                io.open(self.redirection_file_path, 'w+').close()
            # Write to the file if needed
            if self.buffered_text is not None:
                with io.open(self.redirection_file_path, self._file_mode) as f:
                    print(self.buffered_text, '\n', sep='', file=f)
        self.buffered_text = None
