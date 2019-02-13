"""
Module `chatette.cli.interactive_commands.exit_command`.
Contains the strategy class that represents the interactive mode command
`exit` which exits the interactive mode.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExitCommand(CommandStrategy):

    def execute(self, facade):
        pass

    def should_exit(self):
        return True


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
