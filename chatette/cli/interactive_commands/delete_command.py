"""
Module `chatette.cli.interactive_commands.delete_command`.
Contains the strategy class that represents the interactive mode command
`delete` which deletes a unit declaration from the parser.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class DeleteCommand(CommandStrategy):
    usage_str = 'delete <unit-type> "<unit-name>"'
    def __init__(self, command_str, quiet=False):
        super(DeleteCommand, self).__init__(command_str, quiet)
        self._units_to_delete = []

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        self._units_to_delete.append((unit_type, unit_name, variation_name))
        self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                unit_name + "' was successfully deleted.")

    def finish_execution(self, facade):
        for (unit_type, unit_name, variation_name) in self._units_to_delete:
            try:
                facade.parser.delete(unit_type, unit_name, variation_name)
            except KeyError:
                self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                        unit_name + "' was not defined.")
        self._units_to_delete = []
