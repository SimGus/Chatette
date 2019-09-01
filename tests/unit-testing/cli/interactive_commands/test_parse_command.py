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
    new_facade()

    cmd = ParseCommand("error")
    assert cmd.command_tokens == ["error"]
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing template file path\n" + \
           "\tUsage: 'parse <file_path>'" in captured.out


def test_execute(capsys):
    cmd = \
        ParseCommand(
            "parse tests/unit-testing/cli/interactive_commands/other.chatette"
        )
    assert cmd.command_tokens == [
        "parse", "tests/unit-testing/cli/interactive_commands/other.chatette"
    ]
    cmd.execute()
    captured = capsys.readouterr()
    assert "tests/unit-testing/cli/interactive_commands/other.chatette" in captured.out


def test_abstract_methods():
    cmd = ParseCommand('exit')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution()
