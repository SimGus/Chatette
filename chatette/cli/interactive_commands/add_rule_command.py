"""
Module `chatette.cli.interactive_commnads.add_rule_command`.
Contains the strategy class that represents the interactive mode command
`add-rule` which allows to add a rule to a unit definition.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class AddRuleCommand(CommandStrategy):
    usage_str = 'add-rule <unit-type> "<unit-name>" "<rule>"'

    def execute(self, facade):
        # TODO support variations
        if len(self.command_tokens) < 4:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         self.usage_str)
            return

        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_regex = self.get_name_as_regex(self.command_tokens[2])
        rule_str = CommandStrategy.remove_quotes(self.command_tokens[3])
        if unit_regex is None:
            unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
            self._add_rule(facade.parser, unit_type, unit_name, rule_str)
        else:
            count = 0
            for unit_name in self.next_matching_unit_name(facade.parser,
                                                          unit_type,
                                                          unit_regex):
                self._add_rule(facade.parser, unit_type, unit_name, rule_str)
                count += 1
            if count == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

    def _add_rule(self, parser, unit_type, unit_name, rule_str):
        rule_tokens = parser.tokenizer.tokenize(rule_str)
        rule = parser.tokens_to_sub_rules(rule_tokens)

        unit = parser.get_definition(unit_name, unit_type)
        unit.add_rule(rule)

        self.print_wrapper.write("Rule successfully added to " +
                                 unit_type.name + " '" + unit_name + "'.")
