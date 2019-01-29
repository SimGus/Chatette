"""
Module `chatette.terminal_writer`.
Contains a wrapper of the output of commands, that can write to the terminal
(stdout) or to a file.
"""

from __future__ import print_function
import io


class TerminalWriter(object):
    """Wrapper of `print` that can write to stdout or to a file."""
    def __init__(self):
        self.redirection_file_path = None

    def reset(self):
        self.redirection_file_path = None
    
    def write(self, text):
        if self.redirection_file_path is None:
            print(text)
        else:
            with io.open(self.redirection_file_path, 'a+') as f:
                print(text, '\n', sep='', file=f)
