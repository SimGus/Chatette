"""
Module `chatette.cli.interactive_commands.definition_command`.
Contains the strategy class that represents the interactive mode command
`examples` which generates several (or all) possible examples for a given unit.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExamplesCommand(CommandStrategy):
    def __init__(self, command_str):
        super(ExamplesCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `examples`, which generates a certain number of
        possible examples for a given unit definition.
        """
        # TODO support variation names and argument values
        if len(self.command_tokens) < 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'examples <unit-type> "<unit-name>" ' +
                                         "[<number-examples>]")
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
        nb_examples = None  # All examples should be generated
        if len(self.command_tokens) > 3:
            try:
                nb_examples = int(self.command_tokens[3])
            except ValueError:
                self.print_wrapper.error_log("The number of examples to be " +
                                             "generated is invalid: it must " +
                                             "be an integer (no other " +
                                             "characters allowed).")
                return
        try:
            definition = facade.parser.get_definition(unit_name, unit_type)
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is not defined.")
        examples = definition.generate_nb_examples(nb_examples)
        self.print_wrapper.write("Examples for " + unit_type.name + " '" +
                                 unit_name + "':")
        for ex in examples:
            self.print_wrapper.write(ex)

