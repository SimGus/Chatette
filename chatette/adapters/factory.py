"""
Module `chatette.adapters.factory`.
Defines a factory method that allows to create an adapter from a string name.
"""

from chatette.adapters.jsonl import JsonListAdapter
from chatette.adapters.rasa import RasaAdapter


def create_adapter(adapter_name):
    """
    Instantiate an adapter and returns it given the name of the adapter as a str.
    Names are:
        - 'rasa': RasaAdapter
        - 'jsonl': JsonListAdapter
    """
    if adapter_name is None:
        return None
    adapter_name = adapter_name.lower()
    if adapter_name == 'rasa':
        return RasaAdapter()
    elif adapter_name == 'jsonl':
        return JsonListAdapter()
    raise ValueError("Unknown adapter was selected.")
