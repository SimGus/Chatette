#!/usr/bin/env python3

from utils import *


def to_Rasa_format(intent_name, example):
    # ({"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}) -> ({"text": str, "intent": str, "entities": [...]})
    example_str = example["text"]
    entities = example["entities"]

    rasa_entities = []
    for entity in entities:
        first_index = example_str.find(entity["text"])
        rasa_entities.append({
            "value": entity["value"],
            "entity": entity["slot-name"],
            "start": first_index,
            "end": first_index+len(entity["text"]),
        })

    return {
        "text": example_str,
        "intent": intent_name,
        "entities": rasa_entities,
    }
