"""
Module `chatette.terminal_writer`.
Contains a wrapper of the output of commands, that can write to the terminal
(stdout) or to a file.
"""

from __future__ import print_function
import io
from enum import Enum


class RedirectionType(Enum):  # QUESTION is it possible to merge this with relevant strings?
    truncate = 1
    append = 2


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
        if redirection_type == RedirectionType.append:
            self.file_mode = 'a+'
        else:
            self.file_mode = 'w+'
    
    def write(self, text):
        print("redir", self.redirection_file_path)
        print("mode", self.file_mode)
        if self.redirection_file_path is None:
            print(text)
        else:
            if self.buffered_text is None:
                self.buffered_text = text
            else:
                self.buffered_text +='\n' + text
    
    def flush(self):
        """
        Flushes the buffered text to the redirection file
        if such a file is provided.
        """
        if self.redirection_file_path is not None:
            with io.open(self.redirection_file_path, self.file_mode) as f:
                print(self.buffered_text, '\n', sep='', file=f)
    
    def error_log(self, text):
        processed_text = ''.join(['\t' + line for line in text.split('\n')])
        self.write("[ERROR]"+processed_text)
