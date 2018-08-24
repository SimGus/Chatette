#!/usr/bin/env python3

from utils import *


def to_Rasa_format(intent_name, example):
    # ({"text": str, "entities": [{"slot-name": str, "text": str, "value": str}]}) -> ({"text": str, "intent": str, "entities": [...]})
    example_str = example["text"]
    entities = example["entities"]

    rasa_entities = []
    for entity in entities:
        first_index = example_str.find(entity["text"].strip())  # Always finds something
        if first_index == -1:
            print("couldn't find '"+entity["text"].strip()+"' in '"+example_str+"'")
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
