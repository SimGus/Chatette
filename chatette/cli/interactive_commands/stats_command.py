"""
Module `chatette.cli.interactive_commands.stats_command`.
Contains the strategy class that represents the interactive mode command
`stats` which shows statistics about the parsing.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy


class StatsCommand(CommandStrategy):

    def execute(self, facade):
        """Implements the command `stats`, printing parsing statistics."""
        self.print_wrapper.write("Statistics:")
        stats = facade.get_stats_as_str()
        self.print_wrapper.write(stats)


    # Override abstract methods
    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()
    def finish_execution(self, facade):
        raise NotImplementedError()
