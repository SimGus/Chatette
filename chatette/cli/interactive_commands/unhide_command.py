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
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'unhide <unit-type> "<unit-name>"')
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        if unit_type is None:
            self.print_wrapper.error_log("Unknown unit type: '" +
                                         str(self.command_tokens[1]) + "'.")
            return

        unit_regex = self.get_regex_name(self.command_tokens[2])
        if unit_regex is None:
            try:
                [unit_name, variation_name] = \
                    CommandStrategy.split_exact_unit_name(self.command_tokens[2])
            except SyntaxError:
                self.print_wrapper.error_log("Unit identifier couldn't be " + \
                                             "interpreted. Did you mean to " + \
                                             "escape some hashtags '#'?")
                return
            self.execute_on_unit(facade, unit_type, unit_name, variation_name)
        else:
            unit_names = [unit_name
                          for unit_name in HideCommand.stored_units[unit_type.name]
                          if unit_regex.match(unit_name)]
            if len(unit_names) == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

            for unit_name in unit_names:
                self.execute_on_unit(facade, unit_type, unit_name)

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        if variation_name is None:
            try:
                unit = HideCommand.stored_units[unit_type.name][unit_name]
                facade.parser.add_definition(unit_type, unit_name, unit)
                del HideCommand.stored_units[unit_type.name][unit_name]
                self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                        unit_name + "' was successfully restored.")
            except KeyError:
                self.print_wrapper.error_log(unit_type.name.capitalize() + " '" +
                                             unit_name + "' was not " +
                                             "previously hidden.")
            except ValueError:
                self.print_wrapper.error_log(unit_type.name.capitalize() + " '" +
                                             unit_name + "' is already defined " +
                                             "in the parser.")
        else:
            unit = None
            try:
                unit = facade.parser.get_definition(unit_name, unit_type)
            except KeyError:
                self.print_wrapper.error_log(unit_type.name.capitalize() + " '" + \
                                             unit_name + "' is not defined.")
                return
            try:
                rules = \
                    HideCommand.stored_variations[unit_type.name][unit_name][variation_name]
                if variation_name in unit.variations:
                    self.print_wrapper.error_log("Variation '" + variation_name + \
                                                 "' is already defined for " + \
                                                 unit_type.name + " '" + \
                                                 unit_name + "'.")
                    return
                unit.add_rules(rules, variation_name)
                self.print_wrapper.write("Variation '" + variation_name + \
                                         "' of " + unit_type.name + " '" + \
                                         unit_name + "' was successfully restored.")
            except KeyError:
                self.print_wrapper.error_log("Variation '" + variation_name + \
                                             "' of " + unit_type.name + " '" + \
                                             unit_name + "' was not " + \
                                             "previously hidden.")


    # Override abstract methods
    def finish_execution(self, facade):
        raise NotImplementedError()
