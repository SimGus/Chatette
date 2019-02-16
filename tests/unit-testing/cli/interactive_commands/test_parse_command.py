"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.parse_command`.
"""

import pytest

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.parse_command import ParseCommand

from test_command_strategy import new_facade


def test_obj():
    cmd = ParseCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = ParseCommand("parse file")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["parse", "file"]


def test_err(capsys):
    cmd = ParseCommand("error")
    assert cmd.command_tokens == ["error"]
    cmd.execute(new_facade())
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing template file path\n" + \
           "\tUsage: 'parse <filepath>'" in captured.out


def test_execute(capsys):
    cmd = ParseCommand(
            "parse tests/unit-testing/cli/interactive_commands/toilets.chatette"
        )
    assert cmd.command_tokens == \
        ["parse",
         "tests/unit-testing/cli/interactive_commands/toilets.chatette"]
    cmd.execute(new_facade())
    captured = capsys.readouterr()
    assert "[DBG] Parsing master file: " + \
           "tests/unit-testing/cli/interactive_commands/toilets.chatette\n" + \
           "[DBG] Parsing finished!" in captured.out


def test_abstract_methods():
    cmd = ParseCommand('exit')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution(None)
