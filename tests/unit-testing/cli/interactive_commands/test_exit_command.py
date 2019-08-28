"""
Test module.
Tests the functionalities in module
`chatette.cli.interactive_commands.exit_command`.
"""

import pytest

from chatette.cli.interactive_commands.exit_command import *


def test_obj():
    cmd = ExitCommand('this is "a test"')
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["this", "is", '"a test"']

    cmd = ExitCommand("exit > redirection")
    assert cmd.command_tokens == ["exit"]
    assert cmd.print_wrapper.redirection_file_path == "redirection"

def test_execute(capsys):
    cmd = ExitCommand("")
    cmd.execute()
    captured = capsys.readouterr()
    assert captured.out == ""

def test_should_exit():
    cmd = ExitCommand("")
    assert cmd.should_exit()


def test_abstract_methods():
    cmd = ExitCommand('exit')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution()
