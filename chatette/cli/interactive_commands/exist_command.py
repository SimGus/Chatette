"""
Module `chatette.cli.interactive_commands.exist_command`.
Contains the strategy class that represents the interactive mode command
`exist` which verifies whether a unit is declared or not.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExistCommand(CommandStrategy):
    def __init__(self, command_str):
        super(ExistCommand, self).__init__(command_str)
    
    def execute(self, facade):
        """
        Implements the command `exist`, which checks whether a unit is defined
        and prints some information about it if it does.
        """
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments -- usage:\n"+
                                         'exist <unit-type> "<unit-name>"')
            return
        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str())
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" + 
                                     unit_name + "' is not defined.")
