"""
Module `chatette.cli.interactive_commands.exit_command`.
Contains the strategy class that represents the interactive mode command
`exit` which exits the interactive mode.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExitCommand(CommandStrategy):
    def __init__(self, command_str):
        super(ExitCommand, self).__init__(command_str)

    def execute(self, facade):
        pass

    def should_exit(self):
        return True
