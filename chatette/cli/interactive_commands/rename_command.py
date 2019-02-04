"""
Module `chatette.cli.interactive_commands.rename_command`.
Contains the strategy class that represents the interactive mode command
`rename` which changes the name of a unit (if it exists).
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class RenameCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `rename` which renames a unit
        into something else. Displays an error if the unit wasn't found.
        """
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log("Missing some arguments -- usage:\n" +
                                         'rename <unit-type> "<old-name>" ' +
                                         '"<new-name>"')
            return
        unit_type = \
            CommandStrategy.get_unit_type_from_str(self.command_tokens[1])

        if unit_type is None:
            self.print_wrapper.error_log("Unknown unit type: '" +
                                         str(self.command_tokens[1]) + "'.")
        else:
            old_name = CommandStrategy.remove_quotes(self.command_tokens[2])
            new_name = CommandStrategy.remove_quotes(self.command_tokens[3])
            try:
                facade.parser.rename_unit(unit_type, old_name, new_name)
                self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                         old_name + "' was successfully " +
                                         "renamed to '" + new_name + "'.")
            except KeyError:
                self.print_wrapper.error_log("Couldn't find a unit named '" +
                                             str(old_name) + "'.")
