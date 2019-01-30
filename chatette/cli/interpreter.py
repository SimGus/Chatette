"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function

from chatette import __version__
from chatette.cli.terminal_writer import TerminalWriter
from chatette.utils import print_DBG
from chatette.parsing.parser_utils import UnitType


REDIRECTION_SYM = ">"
REDIRECTION_APPEND_SYM = ">>"  # TODO use this


class CommandLineInterpreter(object):
    def __init__(self, facade):
        self.facade = facade
        self.print_wrapper = TerminalWriter()
        self.introduce()

    def introduce(self):
        """
        Tells the user they are in interactive mode and
        asks the facade to execute the parsing of the master file if needed.
        """
        print("Chatette v"+__version__+" running in *interactive mode*.")
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
        print_DBG("redirect: "+str(self.print_wrapper.redirection_file_path))
        operation_name = command_tokens[0].lower()
        if operation_name == "exit":
            return True
        elif operation_name == "stats":
            self.print_stats()
        elif operation_name == "parse":
            self.parse(command_tokens[1])
        elif operation_name == "exist":
            self.verify_unit_existence(command_tokens)
        elif operation_name == "rename":
            self.rename_unit(command_tokens)
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

    @staticmethod
    def get_unit_type_from_str(unit_type_str):
        """
        Transforms the string `unit_type_str`
        into the corresponding `UnitType` value.
        Returns `None` if there exist no corresponding `UnitType` value.
        """
        unit_type_str = unit_type_str.lower()
        if unit_type_str == "alias":
            return UnitType.alias
        elif unit_type_str == "slot":
            return UnitType.slot
        elif unit_type_str == "intent":
            return UnitType.intent
        return None

    @staticmethod
    def remove_quotes(text):
        """
        Remove the double quotes at the beginning and end of `text` and
        remove the escapement of other quotes.
        """
        return text[1:-1].replace(r'\"', '"')


    def print_stats(self):
        """Implements the command `stats`, printing parsing statistics."""
        self.print_wrapper.write("Statistics:")
        if self.facade is None:
            self.print_wrapper.write("\tNo file parsed.")
        else:
            stats = self.facade.get_stats_as_str()
            self.print_wrapper.write(stats)
    
    def parse(self, filepath):
        """
        Implements the command `parse`,
        parsing the template file at `filepath` using the current parser.
        """
        self.facade.parse_file(filepath)

    def verify_unit_existence(self, tokens):
        """
        Implements the command `exist`, which checks whether a unit is defined
        and prints some information about it if it does.
        """
        if len(tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments -- usage:\n"+
                                         'exist <unit-type> "<unit-name>"')
            return
        unit_type = CommandLineInterpreter.get_unit_type_from_str(tokens[1])
        unit_name = CommandLineInterpreter.remove_quotes(tokens[2])
        try:
            unit = self.facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str())
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" + 
                                     unit_name + "' is not defined.")
    
    def rename_unit(self, tokens):
        """
        Implements the command `rename` which renames a unit
        into something else. Displays an error if the unit wasn't found.
        """
        if len(tokens) < 4:
            self.print_wrapper.error_log("Missing some arguments -- usage:\n"+
                                         'rename <unit-type> "<old-name>" '+
                                         '"<new-name>"')
            return
        unit_type = CommandLineInterpreter.get_unit_type_from_str(tokens[1])
        if unit_type is None:
            self.print_wrapper.error_log("Unknown unit type: '"+str(tokens[1])+"'.")
        else:
            old_name = CommandLineInterpreter.remove_quotes(tokens[2])
            new_name = CommandLineInterpreter.remove_quotes(tokens[3])
            try:
                self.facade.parser.rename_unit(unit_type, old_name, new_name)
            except KeyError:
                self.print_wrapper.error_log("Couldn't find a unit named '"+
                                             str(old_name)+"'.")
        
