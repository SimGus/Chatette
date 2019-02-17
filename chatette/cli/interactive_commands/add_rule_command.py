"""
Module `chatette.cli.interactive_commands.add_rule_command`.
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
        if unit_type is None:
            self.print_wrapper.error_log("Unknown unit type: '" +
                                         str(self.command_tokens[1]) + "'.")
            return

        unit_regex = self.get_regex_name(self.command_tokens[2])
        rule_str = CommandStrategy.remove_quotes(self.command_tokens[3])
        if unit_regex is None:
            try:
                [unit_name, variation_name] = \
                    CommandStrategy.split_exact_unit_name(self.command_tokens[2])
            except SyntaxError:
                self.print_wrapper.error_log("Unit identifier couldn't be " + \
                                             "interpreted. Did you mean to " + \
                                             "escape some hashtags '#'?")
                return
            self._add_rule(facade.parser, unit_type, unit_name, variation_name,
                           rule_str)
        else:
            count = 0
            for unit_name in self.next_matching_unit_name(facade.parser,
                                                          unit_type,
                                                          unit_regex):
                self._add_rule(facade.parser, unit_type, unit_name, None,
                               rule_str)
                count += 1
            if count == 0:
                self.print_wrapper.write("No " + unit_type.name + " matched.")

    def _add_rule(self, parser, unit_type, unit_name, variation_name, rule_str):
        rule_tokens = parser.tokenizer.tokenize(rule_str)
        rule = parser.tokens_to_sub_rules(rule_tokens)

        unit = parser.get_definition(unit_name, unit_type)
        unit.add_rule(rule, variation_name)

        self.print_wrapper.write("Rule successfully added to " +
                                 unit_type.name + " '" + unit_name + "'.")


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
