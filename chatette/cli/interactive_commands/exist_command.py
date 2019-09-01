"""
Module `chatette.cli.interactive_commands.exist_command`.
Contains the strategy class that represents the interactive mode command
`exist` which verifies whether a unit is declared or not.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy

from chatette.units.ast import AST


class ExistCommand(CommandStrategy):
    usage_str = 'exist <unit-type> "<unit-name>"'

    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        try:
            unit = AST.get_or_create()[unit_type][unit_name]
            self.print_wrapper.write(unit.short_description())
            if variation_name is not None:
                if variation_name in unit._variation_rules:
                    self.print_wrapper.write(
                        "Variation '" + variation_name + \
                        "' is defined for this " + unit.unit_type.name + "."
                    )
                else:
                    self.print_wrapper.write(
                        "Variation '" + variation_name + \
                        "' is not defined for this " + unit.unit_type.name + "."
                    )
        except KeyError:
            self.print_wrapper.write(
                unit_type.name.capitalize() + " '" + unit_name + \
                "' is not defined."
            )
        self.print_wrapper.write("")