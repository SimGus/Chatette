#!/usr/bin/env python3

from utils import *


def to_Rasa_format(intent_name, example, entities):
    rasa_entities = []
    for entity in entities:
        first_index = example.find(entity["text"].strip())  # Always finds something
        rasa_entities.append({
            "value": entity["value"],
            "entity": entity["slot-name"],
            "start": first_index,
            "end": first_index+len(entity["text"]),
        })

    return {
        "text": example,
        "intent": intent_name,
        "entities": rasa_entities,
    }

def to_Rasa_synonym_format(synonyms):
    # {str: [str]} -> [{"value": str, "synonyms": [str]}]
    rasa_synonyms = []
    for slot_name in synonyms:
        rasa_synonyms.append({
            "value": slot_name,
            "synonyms": synonyms[slot_name],
        })
    return rasa_synonyms
