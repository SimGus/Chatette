"""
Module `chatette.cli.interactive_commands.generate_command`.
Contains the strategy class that represents the interactive mode command
`generate` which generates units and writes them out formatted using a
given adapter.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.adapters.factory import create_adapter


class GenerateCommand(CommandStrategy):
    def __init__(self, command_str):
        super(GenerateCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `generate` which generates all possible examples
        of a certain unit, formatted according to a certain adapter.
        """
        if len(self.command_tokens) == 1:
            facade.run_generation()
            return
        if len(self.command_tokens) == 2:
            try:
                facade.run_generation(self.command_tokens[1])
            except ValueError:
                self.print_wrapper.write("Unknown adapter: '" +
                                         self.command_tokens[1] + "'")
            return
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'generate <adapter> <unit-type> '+
                                         '"<unit-name>"')
            return

        adapter_str = self.command_tokens[1]
        adapter = create_adapter(adapter_str)

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[2])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[3])

        definition = facade.parser.get_definition(unit_name, unit_type)
        examples = definition.generate_all()

        self.print_wrapper.write("Generated examples:")
        for ex in examples:
            # HACK: add a name of intent as ex is not especially a IntentExample
            if not hasattr(ex, 'name'):
                ex.name = "INTERACTIVE"
            self.print_wrapper.write(adapter.prepare_example(ex))