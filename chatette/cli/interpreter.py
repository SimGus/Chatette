"""
Module `chatette.cli`
Contains the interpreter that runs in a terminal in interactive mode.
"""

from __future__ import print_function

from chatette import __version__
from chatette.utils import print_DBG

from chatette.cli.interactive_commands import exit_command, stats_command, \
                                              parse_command, exist_command, \
                                              rename_command


class CommandLineInterpreter(object):
    def __init__(self, facade):
        self.facade = facade
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
        while True:
            print(">>> ", end='')
            try:
                command_str = input()
            except EOFError:
                break
            print_DBG("Got: '"+command_str+"'")
            command = CommandLineInterpreter.get_command(command_str)
            if command is None:
                continue
            if command.should_exit():
                break
            command.execute(self.facade)

    @staticmethod
    def get_command(command_str):
        """Factory method: creates the right command from the provided str."""
        operation_name = command_str.split(maxsplit=1)[0].lower()
        if operation_name == "exit":
            return exit_command.ExitCommand(command_str)
        if operation_name == "stats":
            return stats_command.StatsCommand(command_str)
        if operation_name == "parse":
            return parse_command.ParseCommand(command_str)
        if operation_name == "exist":
            return exist_command.ExistCommand(command_str)
        if operation_name == "rename":
            return rename_command.RenameCommand(command_str)
        else:
            print("Unknown command")
        return None
    