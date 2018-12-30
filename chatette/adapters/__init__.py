"""
Module `adapters`
Contains all the adapters, i.e. the classes
responsible for transforming the generated examples
into output file(s).
"""

from ._base import (Adapter, Batch)
from .jsonl import (JsonListAdapter, )
from .rasa import (RasaAdapter, )

