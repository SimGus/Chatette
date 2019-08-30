# coding: utf-8
"""
Module `chatette.cli.interactive_commands.delete_command`.
Contains the strategy class that represents the interactive mode command
`delete` which deletes a unit declaration from the parser.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy

from chatette.units.ast import AST


class DeleteCommand(CommandStrategy):
    usage_str = 'delete <unit-type> "<unit-name>"'  # TODO support variations
    def __init__(self, command_str, quiet=False):
        super(DeleteCommand, self).__init__(command_str, quiet)
        self._units_to_delete = []

    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        self._units_to_delete.append((unit_type, unit_name, variation_name))

    def finish_execution(self):
        for (unit_type, unit_name, variation_name) in self._units_to_delete:
            try:
                AST.get_or_create().delete_unit(
                    unit_type, unit_name, variation_name
                )
                self.print_wrapper.write(
                    unit_type.name.capitalize() + " '" + unit_name + \
                    "' was successfully deleted."
                )
            except KeyError:
                self.print_wrapper.write(
                    unit_type.name.capitalize() + " '" + unit_name + \
                    "' was not defined."
                )
        self._units_to_delete = []
