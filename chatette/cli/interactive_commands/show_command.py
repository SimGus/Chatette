"""
Module `chatette.cli.interactive_commands.show_command`.
Contains the strategy class that represents the interactive mode command
`show` which shows information about a unit definition and lists a bunch of
its rules (all if possible).
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy

from chatette.units.ast import AST


class ShowCommand(CommandStrategy):
    usage_str = 'show <unit-type> "<unit-name>"'
    max_nb_rules_to_display = 12

    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        try:
            unit = AST.get_or_create()[unit_type][unit_name]
            self.print_wrapper.write(unit.short_description())

            if variation_name is None:
                self.print_wrapper.write(
                    "Template rules:\n" + str(unit.as_template_str())
                )
            else:  # TODO
                pass
        except KeyError:
            self.print_wrapper.write(
                unit_type.name.capitalize() + " '" + unit_name + \
                "' is not defined."
            )
