"""
Test module
Tests the functionalities that are contained in module
`chatette.cli.interactive_commands.stats_command`.
"""

import pytest

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.stats_command import StatsCommand


def test_obj():
    cmd = StatsCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = StatsCommand("stats")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["stats"]


def test_execute(capsys):
    cmd = StatsCommand('stats')
    assert cmd.command_tokens == ["stats"]
    cmd.execute()
    captured = capsys.readouterr()
    assert "Statistics:\n\t1 files parsed\n\t9 declarations: " + \
           "1 intents, 2 slots and 6 aliases\n\t25 rules" in captured.out


def test_abstract_methods():
    cmd = StatsCommand('stats')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution()
