"""
Module `chatette.cli.interactive_commands.definition_command`.
Contains the strategy class that represents the interactive mode command
`examples` which generates several (or all) possible examples for a given unit.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class ExamplesCommand(CommandStrategy):
    usage_str = 'examples <unit-type> "<unit-name>" [<number-examples>]'
    def __init__(self, command_str, quiet=False):
        super(ExamplesCommand, self).__init__(command_str, quiet)
        self.nb_examples = None

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        if self.nb_examples is None:  # Caching the parsed number
            self.nb_examples = -1  # All examples should be generated
            if len(self.command_tokens) > 3:
                try:
                    self.nb_examples = int(self.command_tokens[3])
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
            return
        if self.nb_examples != -1:
            examples = definition.generate_nb_examples(self.nb_examples,
                                                       variation_name)
        else:
            examples = definition.generate_nb_examples(None, variation_name)
        self.print_wrapper.write("Examples for " + unit_type.name + " '" +
                                 unit_name + "':")
        for ex in examples:
            self.print_wrapper.write(ex)
        self.print_wrapper.write("")

    def finish_execution(self, facade):
        self.nb_examples = None
