"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function

from chatette import __version__
from chatette.cli.terminal_writer import TerminalWriter
from chatette.utils import print_DBG


REDIRECTION_SYM = ">"


class CommandLineInterpreter(object):
    def __init__(self, facade=None):
        self.facade = facade
        self.print_wrapper = TerminalWriter()
        self.introduce()

    def introduce(self):
        """
        Tells the user they are in interactive mode and
        asks the facade to execute the parsing of the master file if needed.
        """
        print("Chatette v"+__version__+" running in *interactive mode*.")
        if self.facade is not None:
            self.facade.run_parsing()

    
    def wait_for_input(self):
        stop = False
        while not stop:
            self.print_wrapper.reset()
            print(">>> ", end='')
            try:
                command_str = input()
            except EOFError:
                break
            print_DBG("Got: '"+command_str+"'")
            command_tokens = command_str.split()
            stop = self.interpret(command_tokens)
    
    def interpret(self, command_tokens):
        """
        Calls the right function given the operation's name.
        Returns `True` if the loop should be stopped.
        """
        self.print_wrapper.redirection_file_path = \
            CommandLineInterpreter.find_redirection_file_path(command_tokens)
        print_DBG("redirect: "+self.print_wrapper.redirection_file_path)
        operation_name = command_tokens[0].lower()
        if operation_name == "exit":
            return True
        elif operation_name == "stats":
            self.print_stats()
        elif operation_name == "parse":
            print("Parse (not yet supported)")
        else:
            print("Unknown command")
        return False

    @staticmethod
    def find_redirection_file_path(tokens):
        """
        Finds the path of the file
        which the output of a command should be redirected to and
        returns it. Returns `None` if no redirection was found.
        """
        if len(tokens) < 3 or tokens[-2] != REDIRECTION_SYM:
            return None
        return tokens[-1]


    def print_stats(self):
        """Implements the command `stats`, printing parsing statistics."""
        self.print_wrapper.write("Statistics:")
        if self.facade is None:
            self.print_wrapper.write("\tNo file parsed.")
        else:
            stats = self.facade.get_stats_as_str()
            self.print_wrapper.write(stats)

