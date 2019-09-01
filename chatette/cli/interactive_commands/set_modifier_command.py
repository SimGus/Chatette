"""
Module `chatette.cli.interactive_commands.set_modifier_command`.
Contains the strategy class that represents the interactive mode command
`set-modifier` which allows to change the value of the modifier of a unit
declaration.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.utils import str_to_bool
from chatette.parsing.utils import \
    CASE_GEN_SYM, ARG_SYM, RAND_GEN_SYM, RAND_GEN_PERCENT_SYM

from chatette.units.ast import AST


class SetModifierCommand(CommandStrategy):
    usage_str = \
        'set-modifier <unit-type> "<unit-type>" ' + '<modifer-name> "<value>"'

    def execute(self):
        if len(self.command_tokens) < 5:
            self.print_wrapper.error_log(
                "Missing some arguments\nUsage: " + self.usage_str
            )
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        if unit_type is None:
            self.print_wrapper.error_log(
                "Unknown unit type: '" + str(self.command_tokens[1]) + "'."
            )
            return

        unit_regex = self.get_regex_name(self.command_tokens[2])

        modifier_name = self.command_tokens[3]
        # TODO this is not the best way to get the value
        modifier_value = \
            CommandStrategy.split_exact_unit_name(self.command_tokens[4])[0]

        if unit_regex is None:
            try:
                [unit_name, variation_name] = \
                    CommandStrategy.split_exact_unit_name(
                        self.command_tokens[2]
                    )
            except SyntaxError:
                self.print_wrapper.error_log(
                    "Unit identifier couldn't be interpreted. " + \
                    "Did you mean to escape some hashtags '#'?"
                )
                return
            if variation_name is not None:
                self.print_wrapper.error_log(
                    "Cannot set a modifier for the variation of a unit."
                )
                return
            self._set_modifier(
                unit_type, unit_name, modifier_name, modifier_value
            )
        else:
            count = 0
            for unit_name in self.next_matching_unit_name(
                unit_type, unit_regex
            ):
                self._set_modifier(
                    unit_type, unit_name, modifier_name, modifier_value
                )
                count += 1
            if count == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

    def _set_modifier(self, unit_type, unit_name, modifier_name, value):
        unit = AST.get_or_create()[unit_type][unit_name]
        modifier_name = modifier_name.lower()
        if modifier_name in ("casegen", CASE_GEN_SYM):
            try:
                value = str_to_bool(value)
                unit.set_casegen(value)
            except ValueError:
                self.print_wrapper.write(
                    "Invalid value for case generation modifier " + \
                    "(True or False)."
                )
                return
        elif modifier_name in ("arg", ARG_SYM):
            unit.set_arg_value(value)
        elif modifier_name in ("randgen", RAND_GEN_SYM):
            try:
                value = str_to_bool(value)
                unit.set_randgen(value)
            except ValueError:
                self.print_wrapper.write(
                    "Invalid value for random generation modifier " + \
                    "(True or False)."
                )
                return
        elif modifier_name in "randgen-name":
            unit.set_randgen_name(modifier_name)
        elif modifier_name in ("randgen-percent", RAND_GEN_PERCENT_SYM):
            try:
                value = float(value)
                unit.set_randgen_percent(value)
            except ValueError:
                self.print_wrapper.write(
                    "Invalid value for the random generation percentage " + \
                    "modifier (expected a float)."
                )
                return
        else:
            self.print_wrapper.write(
                "Invalid modifier selected (can be 'casegen', " + \
                "'randgen', 'randgen-name', 'randgen-percent' or 'arg')."
            )
            return
        self.print_wrapper.write(
            "Modifier for " + unit_type.name + " '" + unit_name + \
            "' successfully changed."
        )


    # Override abstract methods
    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self):
        raise NotImplementedError()
