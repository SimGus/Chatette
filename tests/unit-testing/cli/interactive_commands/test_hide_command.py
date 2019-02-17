"""
Test module.
Tests the functionalities present in module
`chatette.cli.interactive_commands.delete_command`.
"""

import pytest

from test_command_strategy import new_facade

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.hide_command import HideCommand
from chatette.cli.interactive_commands.unhide_command import UnhideCommand
from chatette.parsing.parser_utils import UnitType


def test_obj():
    cmd = HideCommand("")
    assert cmd.command_tokens == []
    assert isinstance(cmd, CommandStrategy)


def test_err(capsys):
    facade = new_facade()
    cmd = HideCommand('hide alias "inexistant"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Alias 'inexistant' was not defined." in captured.out

    cmd = UnhideCommand("unhide")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tMissing some arguments\n\tUsage: " + \
           'unhide <unit-type> "<unit-name>"' in captured.out

    cmd = UnhideCommand('unhide alias "inexistant"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Alias 'inexistant' was not previously hidden." in captured.out

    cmd = UnhideCommand('unhide nothing "a"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Unknown unit type: 'nothing'." in captured.out

    cmd = UnhideCommand('unhide alias "var#a#b"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Unit identifier couldn't be interpreted. " + \
           "Did you mean to escape some hashtags '#'?" in captured.out

    cmd = UnhideCommand("unhide alias /unmatchable/")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "No alias matched." in captured.out


def test_execute(capsys):
    cmd = HideCommand('hide alias "tell me"')
    facade = new_facade()
    try:
        facade.parser.get_definition("tell me", UnitType.alias)
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'tell me' doesn't exist " + \
                    "in the parser.")
    cmd.execute(facade)
    with pytest.raises(KeyError):
        facade.parser.get_definition("tell me", UnitType.alias)
    captured = capsys.readouterr()
    assert "Alias 'tell me' was successfully hidden." in captured.out

    cmd = UnhideCommand('unhided alias "tell me"')
    cmd.execute(facade)
    try:
        facade.parser.get_definition("tell me", UnitType.alias)
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'tell me' wasn't restored.")
    captured = capsys.readouterr()
    assert "Alias 'tell me' was successfully restored."

    cmd = HideCommand("hide ~ /./")
    cmd.execute(facade)
    _ = capsys.readouterr()
    cmd = UnhideCommand("unhide ~ /./")
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Alias 'tell me' was successfully restored." in captured.out
    assert "Alias 'can you' was successfully restored." in captured.out

    # Hide a unit and try to restore it twice
    cmd = HideCommand('hide ~ "can you"')
    facade = new_facade()
    cmd.execute(facade)

    cmd = UnhideCommand('unhide alias "can you"')
    other_facade = new_facade()
    cmd.execute(other_facade)

    captured = capsys.readouterr()
    assert "Alias 'can you' is already defined in the parser." in captured.out


def test_variations(capsys):
    cmd = HideCommand('hide alias "var#one"')
    facade = new_facade()
    cmd.execute(facade)
    try:
        unit = facade.parser.get_definition("var", UnitType.alias)
        assert "one" not in unit.variations
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'var' doesn't exist " + \
                    "in the parser.")

    cmd = UnhideCommand('unhide alias "var#nothing"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Variation 'nothing' of alias 'var' " + \
           "was not previously hidden." in captured.out

    cmd = UnhideCommand('unhide ~ "var#one"')
    cmd.execute(facade)
    try:
        unit = facade.parser.get_definition("var", UnitType.alias)
        assert "one" in unit.variations
    except KeyError:
        pytest.fail("Unexpected KeyError. Alias 'var' doesn't exist " + \
                    "in the parser.")

    cmd = HideCommand('hide ~ "var#nothing"')
    cmd.execute(new_facade())
    captured = capsys.readouterr()
    assert "Couldn't find variation 'nothing' in alias 'var'." in captured.out

    cmd = UnhideCommand('unhide ~ "nothing#var"')
    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "Alias 'nothing' is not defined." in captured.out

    # Hide a variation and try to restore it twice
    cmd = HideCommand('hide ~ "var#one"')
    facade = new_facade()
    cmd.execute(facade)

    cmd = HideCommand('hide ~ "var#one"')
    other_facade = new_facade()
    cmd.execute(other_facade)

    cmd = UnhideCommand('unhide ~ "var#one"')
    assert cmd.command_tokens == ["unhide", "~", '"var#one"']
    cmd.execute(facade)

    cmd.execute(facade)
    captured = capsys.readouterr()
    assert "[ERROR]\tVariation 'one' is " + \
           "already defined for alias 'var'." in captured.out


def test_abstract_methods():
    cmd = UnhideCommand('unhide ~ "var"')
    with pytest.raises(NotImplementedError):
        cmd.finish_execution(None)
