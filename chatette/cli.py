"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function


class CommandLineInterpreter(object):
    def __init__(self, facade=None):
        self.facade = facade
    
    def wait_for_input(self):
        stop = False
        while not stop:
            print(">>> ", end='')
            command_str = input()
            print("Got: '"+command_str+"'")
            command_tokens = command_str.split()
            stop = self.interpret(command_tokens[0].lower())
    
    def interpret(self, operation_name):
        """
        Calls the right function given the operation's name.
        Returns `True` if the loop should be stopped.
        """
        if operation_name == "exit":
            return True
        else:
            print("Unknown command")

