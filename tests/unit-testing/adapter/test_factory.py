"""
Test module.
Tests the functionalities that are present in module
`chatette.adapters.factory`.
"""

import pytest

from chatette.adapters.factory import create_adapter
from chatette.adapters.jsonl import JsonListAdapter
from chatette.adapters.rasa import RasaAdapter


def test_valid():
    assert isinstance(create_adapter("jsonl"), JsonListAdapter)
    assert isinstance(create_adapter("rasa"), RasaAdapter)

def test_invalid():
    assert create_adapter(None) is None
    with pytest.raises(ValueError):
        create_adapter("no adapter")
