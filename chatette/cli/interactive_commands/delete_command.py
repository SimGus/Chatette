"""
Module `chatette.cli.interactive_commands.delete_command`.
Contains the strategy class that represents the interactive mode command
`delete` which deletes a unit declaration from the parser.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class DeleteCommand(CommandStrategy):
    def __init__(self, command_str):
        super(DeleteCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `delete`, which removes a unit declaration
        from the parser of `facade`.
        """
        # TODO allow for deleting variations
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments.\nUsage: " +
                                         'delete <unit-type> "<unit-name>"')
            return
        
        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_regex = CommandStrategy.get_name_as_regex(self.command_tokens[2])
        if unit_regex is None:
            unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
            self._delete_unit(facade.parser, unit_type, unit_name)
        else:
            for unit_name in \
                CommandStrategy.get_all_matching_unit_name(facade.parser,
                                                           unit_type,
                                                           unit_regex):
                self._delete_unit(facade.parser, unit_type, unit_name)
                
    def _delete_unit(self, parser, unit_type, unit_name):
        try:
            parser.delete(unit_type, unit_name)
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                    unit_name + "' was successfully deleted.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                    unit_name + "' was not defined.")

