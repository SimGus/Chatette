"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function

from chatette import __version__


class CommandLineInterpreter(object):
    def __init__(self, facade=None):
        self.facade = facade
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
            print(">>> ", end='')
            command_str = input()
            print("Got: '"+command_str+"'")
            command_tokens = command_str.split()
            stop = self.interpret(command_tokens)
    
    def interpret(self, command_tokens):
        """
        Calls the right function given the operation's name.
        Returns `True` if the loop should be stopped.
        """
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


    def print_stats(self):
        """Implements the command `stats`, printing parsing statistics."""
        print("Statistics:")
        if self.facade is None:
            print("\tNo file parsed.")
        else:
            self.facade.print_stats()

