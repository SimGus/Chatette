"""
Module `chatette.cli.interactive_commands.unhide_command`.
Contains the strategy class that represents the interacive mode command
`unhide` which restores a unit definition that has been hidden.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.hide_command import HideCommand


class UnhideCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `unhide` which restores a unit definition that
        was hidden from the parser of `facade`.
        """
        if len(self.command_tokens) > 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'unhide <unit-type> "<unit-name>"')
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_regex = self.get_name_as_regex(self.command_tokens[2])
        if unit_regex is None:
            unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
            self.execute_on_unit(facade, unit_type, unit_name)
        else:
            unit_names = [unit_name
                          for unit_name in HideCommand.stored_units[unit_type.name]
                          if unit_regex.match(unit_name)]
            if len(unit_names) == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

            for unit_name in unit_names:
                self.execute_on_unit(facade, unit_type, unit_name)

    def execute_on_unit(self, facade, unit_type, unit_name):
        try:
            unit = HideCommand.stored_units[unit_type.name][unit_name]
            facade.parser.add_definition(unit_type, unit_name, unit)
            del HideCommand.stored_units[unit_type.name][unit_name]
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was successfully restored.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was not previously hidden.")
        except ValueError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is already defined " +
                                     "the parser.")
