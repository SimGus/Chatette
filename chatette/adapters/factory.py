"""
Module `chatette.adapters.factory`.
Defines a factory method that allows to create an adapter from a string name.
"""

from chatette.adapters.jsonl import JsonListAdapter
from chatette.adapters.rasa import RasaAdapter
from chatette.adapters.rasa_md import RasaMdAdapter


def create_adapter(adapter_name, base_filepath=None):
    """
    Instantiate an adapter and returns it given the name of the adapter as a str.
    Names are:
        - 'rasa': RasaAdapter
        - 'rasa-md' or 'rasamd': RasaMdAdapter
        - 'jsonl': JsonListAdapter
    """
    if adapter_name is None:
        return None
    adapter_name = adapter_name.lower()
    if adapter_name == 'rasa':
        return RasaAdapter(base_filepath)
    elif adapter_name in ('rasa-md', 'rasamd'):
        return RasaMdAdapter(base_filepath)
    elif adapter_name == 'jsonl':
        return JsonListAdapter(base_filepath)
    raise ValueError("Unknown adapter was selected.")
