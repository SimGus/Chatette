"""
Module `chatette.cli.interactive_commands.generate_command`.
Contains the strategy class that represents the interactive mode command
`generate` which generates units and writes them out formatted using a
given adapter.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.adapters.factory import create_adapter

from chatette.facade import Facade
from chatette.units.ast import AST


class GenerateCommand(CommandStrategy):
    usage_str = 'generate <adapter> <unit-type> "<unit-name>"'
    def __init__(self, command_str, quiet=False):
        super(GenerateCommand, self).__init__(command_str, quiet)
        self.nb_examples = None

    def execute(self):
        """
        Implements the command `generate` which generates all possible examples
        of a certain unit, formatted according to a certain adapter.
        """
        if not Facade.was_instantiated():
            self.print_wrapper.error_log(
                "Cannot generate anything. No file was parsed."
            )
            return
        facade = Facade.get_or_create()
        if len(self.command_tokens) == 1:
            facade.run_generation()
            return
        if len(self.command_tokens) == 2:
            try:
                facade.run_generation(self.command_tokens[1])
            except ValueError:
                self.print_wrapper.write(
                    "Unknown adapter: '" + self.command_tokens[1] + "'"
                )
            return
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log(
                "Missing some arguments\nUsage: " + self.usage_str
            )
            return

        adapter_str = self.command_tokens[1]
        try:
            adapter = create_adapter(adapter_str)
        except ValueError:
            self.print_wrapper.error_log(
                "Unknown adapter '" + adapter_str + "'."
            )

        if len(self.command_tokens) == 5:
            try:
                self.nb_examples = int(self.command_tokens[-1])
            except ValueError:
                self.print_wrapper.error_log(
                    "The number of examples to be generated is invalid: " + \
                    "it must be an integer (no other characters allowed)."
                )
                return

        unit_type = \
            CommandStrategy.get_unit_type_from_str(self.command_tokens[2])
        if unit_type is None:
            self.print_wrapper.error_log(
                "Unknown unit type: '" + str(self.command_tokens[2]) + "'."
            )
            return

        unit_regex = self.get_regex_name(self.command_tokens[3])
        if unit_regex is None:
            print("no regex")
            try:
                [unit_name, variation_name] = \
                    CommandStrategy.split_exact_unit_name(
                        self.command_tokens[3]
                    )
            except SyntaxError:
                self.print_wrapper.error_log(
                    "Unit identifier couldn't be interpreted. " + \
                    "Did you mean to escape some hashtags '#'?"
                )
                return
            self._generate_unit(
                adapter, unit_type, unit_name, variation_name
            )
        else:
            count = 0
            for unit_name in self.next_matching_unit_name(
                unit_type, unit_regex
            ):
                self._generate_unit(adapter, unit_type, unit_name)
                count += 1
            if count == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")
        self.finish_execution()

    def _generate_unit(self,
        adapter, unit_type, unit_name, variation_name=None
    ):
        definition = AST.get_or_create()[unit_type][unit_name]
        if self.nb_examples is None:
            examples = definition.generate_all(variation_name=variation_name)
        else:
            examples = definition.generate_nb_possibilities(
                self.nb_examples, variation_name=variation_name
            )

        self.print_wrapper.write(
            "Generated examples for " + unit_type.name + " '" + unit_name + \
            "':'"
        )
        for ex in examples:
            # HACK: add a name of intent as ex is not especially a IntentExample
            if not hasattr(ex, 'intent_name'):
                ex.intent_name = "INTERACTIVE"
            self.print_wrapper.write(adapter.prepare_example(ex))
        self.print_wrapper.write("")

    def finish_execution(self):
        self.nb_examples = None


    # Override abstract methods
    def execute_on_unit(self, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
