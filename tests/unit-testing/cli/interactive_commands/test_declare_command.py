"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.decalre_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.declare_command import DeclareCommand

from chatette.parsing.parser_utils import UnitType


def test_obj():
    cmd = DeclareCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)

    cmd = DeclareCommand("declare alias /a/")
    assert cmd.command_tokens == ["declare", "alias", "/a/"]
    assert isinstance(cmd, CommandStrategy)


def test_err(capsys):
    facade = new_facade()

    cmd = DeclareCommand("declare")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'declare <unit-type> "<unit-name>"' in captured.out

    cmd = DeclareCommand("declare nothing /a/")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tUnknown unit type: 'nothing'." in captured.out

    cmd = DeclareCommand('declare alias "var#a#b"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tUnit identifier couldn't be interpreted. " + \
           "Did you mean to escape some hashtags '#'?" in captured.out

    cmd = DeclareCommand('declare alias "a#var"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tVariation name detected, " + \
           "while units cannot be declared with a variation. " + \
           "Did you mean to escape some hashtags '#'?" in captured.out

    cmd = DeclareCommand('declare alias "var"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Alias 'var' is already defined."


def test_execute(capsys):
    cmd = DeclareCommand('declare alias "machin"')
    facade = new_facade()
    cmd.execute(facade)
    try:
        unit = facade.parser.get_definition("machin", UnitType.alias)
        assert len(unit.variations) == 0
        assert len(unit.rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Alias 'machin' was successfully declared." in captured.out

    cmd = DeclareCommand('declare slot "machin"')
    facade = new_facade()
    cmd.execute(facade)
    try:
        unit = facade.parser.get_definition("machin", UnitType.slot)
        assert len(unit.variations) == 0
        assert len(unit.rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Slot 'machin' was successfully declared." in captured.out

    cmd = DeclareCommand('declare intent "machin"')
    facade = new_facade()
    cmd.execute(facade)
    try:
        unit = facade.parser.get_definition("machin", UnitType.intent)
        assert len(unit.variations) == 0
        assert len(unit.rules) == 0
    except (KeyError, ValueError):
        pytest.fail("Unexpected error, 'declare' command didn't work.")
    
    captured = capsys.readouterr()
    assert "Intent 'machin' was successfully declared." in captured.out


def test_abstract_methods():
    cmd = DeclareCommand('declare alias "a"')
    with pytest.raises(NotImplementedError):
        cmd.execute_on_unit(None, None, None)
    with pytest.raises(NotImplementedError):
        cmd.finish_execution(None)
    
