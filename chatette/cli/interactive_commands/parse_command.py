"""
Module `chatette.cli.interactive_commands.parse_command`.
Contains the strategy class that represents the interactive mode command
`parse` which parses a new template file.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy

from chatette.facade import Facade


class ParseCommand(CommandStrategy):

    def execute(self):
        """
        Implements the command `parse`,
        parsing a new template file using the current parser.
        """
        if len(self.command_tokens) <= 1:
            self.print_wrapper.error_log("Missing template file path\nUsage: " +
                                         "'parse <file_path>'")
            return
        file_path = self.command_tokens[1]

        if Facade.was_instantiated():
            facade = Facade.get_or_create()
            facade.parse_file(file_path)
        else:
            facade = Facade(file_path)
            facade.run_parsing()


    # Override abstract methods
    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self):
        raise NotImplementedError()
