"""
Module `chatette.cli.interactive_commands.parse_command`.
Contains the strategy class that represents the interactive mode command
`parse` which parses a new template file.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ParseCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `parse`,
        parsing a new template file using the current parser.
        """
        if len(self.command_tokens) <= 1:
            self.print_wrapper.error_log("Missing template file path\nUsage: " +
                                         "'parse <filepath>'")
            return
        filepath = self.command_tokens[1]
        facade.parse_file(filepath)


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
