"""
Module `chatette.cli.interactive_commands.exist_command`.
Contains the strategy class that represents the interactive mode command
`exist` which verifies whether a unit is declared or not.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExistCommand(CommandStrategy):
    usage_str = 'exist <unit-type> "<unit-name>"'

    def execute_on_unit(self, facade, unit_type, unit_name):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.print_wrapper.write(unit.short_desc_str()+'\n')
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is not defined.")
