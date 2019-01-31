"""
Module `chatette.cli.interactive_commands.hide_command`.
Contains the strategy class that represents the interactive mode command
`hide` which hides unit definitions (storing them somewhere to be able to 
unhide them later).
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class HideCommand(CommandStrategy):
    stored_units = {"alias": dict(), "slot": dict(), "intent": dict()}
    def __init__(self, command_str):
        super(HideCommand, self).__init__(command_str)
    
    def execute(self, facade):
        """
        Implements the command `hide` which deletes a unit defined
        in the parser of `facade` and stores it somewhere for it to be able
        to be restored.
        """
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'hide <unit-type> "<unit-name>"')
            return
        
        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
        try:
            unit = facade.parser.get_definition(unit_name, unit_type)
            self.stored_units[unit_type.name][unit_name] = unit
            facade.parser.delete(unit_type, unit_name)
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was not defined.")
        print("stored", self.stored_units)
