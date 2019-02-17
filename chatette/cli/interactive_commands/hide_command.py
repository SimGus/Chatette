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
    stored_variations = {"alias": dict(), "slot": dict(), "intent": dict()}
    def __init__(self, command_str, quiet=False):
        super(HideCommand, self).__init__(command_str, quiet)
        self._units_to_delete = []
        self._var_to_delete = []
    
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            if variation_name is None:
                self.stored_units[unit_type.name][unit_name] = unit
                self._units_to_delete.append((unit_type, unit_name))
                self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                        unit_name + "' was successfully hidden.")
            else:
                if variation_name not in unit.variations:
                    self.print_wrapper.error_log("Couldn't find variation '" + \
                                                 variation_name + "' in " + \
                                                 unit_type.name + " '" + \
                                                 unit_name + "'.")
                    return
                self._var_to_delete.append((unit_type, unit_name, variation_name))
                rules = unit.variations[variation_name]
                if unit_name not in self.stored_variations[unit_type.name]:
                    self.stored_variations[unit_type.name][unit_name] = \
                        {variation_name: rules}
                else:
                    self.stored_variations[unit_type.name][unit_name][variation_name] = \
                        rules
                self.print_wrapper.write("Variation '" + variation_name + "' of " + \
                                         unit_type.name + " '" + unit_name + \
                                         "' was successfully hidden.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was not defined.")
    
    def finish_execution(self, facade):
        for (unit_type, unit_name) in self._units_to_delete:
            facade.parser.delete(unit_type, unit_name)
        self._units_to_delete = []

        for (unit_type, unit_name, variation_name) in self._var_to_delete:
            facade.parser.delete(unit_type, unit_name, variation_name)
        self._var_to_delete = []
