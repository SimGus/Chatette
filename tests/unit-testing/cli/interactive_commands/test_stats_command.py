"""
Test module
Tests the functionalities that are contained in module
`chatette.cli.interactive_commands.stats_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.stats_command import StatsCommand


def test_obj():
    new_facade()
    cmd = StatsCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = StatsCommand("stats")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["stats"]


def test_execute(capsys):
    new_facade()
    cmd = StatsCommand('stats')
    assert cmd.command_tokens == ["stats"]
    cmd.execute()
    captured = capsys.readouterr()
    assert "Statistics:" in captured.out
    assert "Parsed files: 1" in captured.out
    assert "Declared units: 7 (9 variations)" in captured.out
    assert "Declared slots: 1 (2 variations)" in captured.out
    assert "Declared aliases: 5 (6 variations)" in captured.out
    assert "Parsed rules: 25" in captured.out


def test_abstract_methods():
    new_facade()
    cmd = StatsCommand('stats')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution()
