#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
   from chatette.utils import *
except ImportError:
   from utils import *

def find_entity(text, entity_str):
    """Finds `entity_str` in `text` ignoring the case of the first non-space"""
    index = text.find(entity_str)
    if index == -1:
        return text.lower().find(entity_str.lower())
    return index


def to_Rasa_format(intent_name, example):
    # ({"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}) -> ({"text": str, "intent": str, "entities": [...]})
    example_str = example["text"]
    entities = example["entities"]

    rasa_entities = []
    for entity in entities:
        entity["text"] = entity["text"].strip()
        first_index = find_entity(example_str, entity["text"])  # Always finds something
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


def to_Rasa_synonym_format(synonyms):
    # {str: [str]} -> [{"value": str, "synonyms": [str]}]
    return [{"value": slot_name, "synonyms": synonyms[slot_name]}
            for slot_name in synonyms if len(synonyms[slot_name]) > 1]
