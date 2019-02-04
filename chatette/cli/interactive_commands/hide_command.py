"""
Module `chatette.cli.interactive_commands.hide_command`.
Contains the strategy class that represents the interactive mode command
`hide` which hides unit definitions (storing them somewhere to be able to
unhide them later).
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class HideCommand(CommandStrategy):
    usage_str = 'hide <unit-type> "<unit-name>"'
    stored_units = {"alias": dict(), "slot": dict(), "intent": dict()}
    def __init__(self, command_str):
        super(HideCommand, self).__init__(command_str)
        self._units_to_delete = []
    
    def execute_on_unit(self, facade, unit_type, unit_name):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.stored_units[unit_type.name][unit_name] = unit
            self._units_to_delete.append((unit_type, unit_name))
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was successfully hidden.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was not defined.")
    
    def finish_execution(self, facade):
        for (unit_type, unit_name) in self._units_to_delete:
            facade.parser.delete(unit_type, unit_name)
        self._units_to_delete = []
