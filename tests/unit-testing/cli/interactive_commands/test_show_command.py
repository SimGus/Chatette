"""
Test module
Tests the functionalities contained in module
`chatette.cli.interactive_commands.show_command`.
"""

import pytest

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.show_command import ShowCommand


def test_obj():
    cmd = ShowCommand("")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == []

    cmd = ShowCommand("show ~ /a/")
    assert isinstance(cmd, CommandStrategy)
    assert cmd.command_tokens == ["show", "~", "/a/"]


def test_err(capsys):
    cmd = ShowCommand("nothing")
    assert cmd.command_tokens == ["nothing"]
    cmd.execute()
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'show <unit-type> "<unit-name>"' in captured.out


def test_execute(capsys):
    cmd = ShowCommand('show alias "sorry"')
    assert cmd.command_tokens == ["show", "alias", '"sorry"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'sorry'\nmodifiers:\n\tNone\n0 variations" in captured.out

    cmd = ShowCommand('show ~ /o/g')
    assert cmd.command_tokens ==  ["show", "~", "/o/g"]
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'can you'\nmodifiers:\n\tNone\n0 variations" in captured.out
    assert "alias: 'sorry'\nmodifiers:\n\tNone\n0 variations" in captured.out
    assert "Rules:" in captured.out

    cmd = ShowCommand('show slot "INEXISTANT"')
    assert cmd.command_tokens == ["show", "slot", '"INEXISTANT"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "Slot 'INEXISTANT' is not defined." in captured.out

    cmd = ShowCommand('show ~ "lots of rules"')
    assert cmd.command_tokens == ["show", "~", '"lots of rules"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'lots of rules'\nmodifiers:\n\tNone\n0 variations" in captured.out
    assert "rule 0" in captured.out
    assert "rule 11" in captured.out
    assert "rule 12" not in captured.out

def test_variation(capsys):
    cmd = ShowCommand('show alias "var#one"')
    assert cmd.command_tokens == ["show", "alias", '"var#one"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "\t- one\n" in captured.out
    assert "\t- two with space\n" in captured.out
    assert "Rules for variation 'one':\n\tone" in captured.out

    cmd = ShowCommand('show alias "var#two with space"')
    assert cmd.command_tokens == ["show", "alias", '"var#two with space"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "\t- two with space\n" in captured.out
    assert "\t- one\n" in captured.out
    assert "Rules for variation 'two with space':\n\ttwo\n\t2" in captured.out
    
    cmd = ShowCommand('show alias "var#no var"')
    assert cmd.command_tokens == ["show", "alias", '"var#no var"']
    cmd.execute()
    captured = capsys.readouterr()
    assert "alias: 'var'\nmodifiers:\n\tNone\n2 variations:\n" in captured.out
    assert "[ERROR]\tVariation 'no var' is not defined in alias var." in captured.out


def test_abstract_methods():
    cmd = ShowCommand('show ~ "test"')
    try:
        cmd.finish_execution()
    except NotImplementedError:
        pytest.fail("Method 'finish_execution' shouldn't have raised a " + \
                    "'NotImplementedError'.")
