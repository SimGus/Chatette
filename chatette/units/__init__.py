# coding: utf-8
"""
Module `chatette.units`
Contains every classes that represent what will be in the Abstract Syntax Tree
(AST) and the rules.
"""

from math import floor


class Example(object):
    """
    Represents an utterance (i.e. an example of an intent)
    that will later on be written in the output file(s).
    """
    def __init__(self, text=None, entities=None):
        if entities is None:
            entities = []
        if text is None:
            text = ""
        
        self.text = text
        self.entities = entities
        self._slot_value = None  # HACK used by slot to prevent code duplication
    
    def __repr__(self):
        # return "<'" + self.text + "' " + str(self.entities) + '>'
        return str(self)
    def __str__(self):
        return \
            "Text: '" + self.text + \
            "'\n\tEntities: " + str(self.entities)

    def as_dict(self):
        result = {"text": self.text, "entities": []}
        if self._slot_value is not None:
            result["slot-value": self._slot_value]  # TODO this looks weird, look into this
        for entity in self.entities:
            result["entities"].append(entity.as_dict())
        return result

    def __hash__(self):
        entities_hash = 0
        for entity in self.entities:
            entities_hash += hash(entity)
        return hash(self.text) * 10000 + entities_hash  # QUESTION not sure this a very good hash

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    def is_dup(self, other):
        """
        Returns `True` if this example is a duplicate of `other`.
        A duplicate is an example with the same text.
        """
        return self.text == other.text
    
    def prepend(self, text_to_prepend):
        """
        Prepends `text_to_prepend` to the example
        and manages the pointer of the entities.
        """
        length = len(text_to_prepend)
        if length == 0:
            return
        self.text = text_to_prepend + self.text
        for entity in self.entities:
            entity._start_index += length
    def append(self, example_to_append):
        """
        Appends the text of `example_to_append` to the example text
        and manages its pointers to entities if needed.
        @post: don't use `example_to_append` any longer.
        """
        starting_index = len(self.text)
        self.text += example_to_append.text
        for entity in example_to_append.entities:
            entity._start_index += starting_index
            self.entities.append(entity)
        
    def remove_leading_space(self):
        """Removes the leading space of `self.text` if there is one."""
        if len(self.text) > 0 and self.text[0].isspace():
            self.text = self.text[1:]
            for entity in self.entities:
                entity._remove_leading_space()


class IntentExample(Example):
    def __init__(self, intent_name, text=None, entities=None):
        super(IntentExample, self).__init__(text, entities)
        self.intent_name = intent_name
    @classmethod
    def from_example(cls, example, intent_name):
        return cls(intent_name, example.text, example.entities)

    def as_dict(self):
        result = super(IntentExample, self).as_dict()
        result["intent-name"] = self.intent_name
        return result
    
    def __repr__(self):
        return \
            "<intent: " + self.intent_name + \
            " '" + self.text + "' " + str(self.entities) + ">"
    def __str__(self):
        return \
            "Intent: '" + self.intent_name + \
            "'\n\tText: '" + self.text + \
            "'\n\tEntities: " + str(self.entities)
    
    def __eq__(self, other):
        if isinstance(other, Example) and not isinstance(other, IntentExample):
            raise TypeError("Tried to compare an Example and an IntentExample")
        return super(IntentExample, self).__eq__(other)

    def __hash__(self):
        example_hash = super(IntentExample, self).__hash__()
        return hash(self.intent_name) * 1000000000 + example_hash  # QUESTION not sure this a very good hash


class Entity(object):
    """
    Represents an entity as it will be contained in examples
    (instances of `Example`).
    """
    def __init__(self, name, length, value=None, start_index=0):
        self.slot_name = name  # name of the entity (not the associated text)
        self.value = value
        self._len = length
        self._start_index = start_index

    def _remove_leading_space(self):
        """
        Adapts the start index and length if needed, after a leading space was
        removed from the example text.
        @returns: `True` if the entity still makes sense.
        """
        if self._start_index == 0:
            self._len -= 1
            if self._len <= 0:
                return False
        else:
            self._start_index -= 1
        return True
    
    def as_dict(self):
        return {
            "slot-name": self.slot_name,
            "value": self.value,
            "start-index": self._start_index,
            "end-index": self._start_index + self._len
        }
    
    def __repr__(self):
        representation = "entity '" + self.slot_name + "'"
        if self.value is not None:
            representation += ":'" + self.value + "'"
        return representation
    def __str__(self):
        return \
            self.slot_name + "@" + str(self._start_index) + "\t=>\t" + str(self.value)
    
    def __hash__(self):
        return \
            hash(self.slot_name +"@" + str(self._start_index) + ":" + str(self.value))
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    

def add_example_no_dup(example_list, new_example):
    """
    Adds `new_example` to the list of examples `example_list`,
    and then removes duplicates.
    An example is a duplicate of another if they have the same text. The one
    that is kept is the one with the largest amount of entities.
    @pre: - `example_list` must be a sorted list (with key == text).
          - `example_list` does not contain duplicates.
    @post: the returned list is sorted.
    """
    # TODO maybe using sets would be a better idea?
    # Find closest example
    lo = 0
    hi = len(example_list) - 1
    i = int(floor(hi/2))
    found = False
    while lo <= hi:
        current_text = example_list[i].text
        if current_text == new_example.text:
            found = True
            break
        elif current_text > new_example.text:
            hi = float(i - 1)
        else:  # current_text < new_example.text
            lo = float(i + 1)
        
        i = int(floor(abs(hi - lo)/2) + lo)

    # Add example if needed
    if not found:
        example_list.insert(i, new_example)
    # Replace example if needed
    elif len(example_list[i].entities) < len(new_example.entities):
        example_list[i] = new_example
    return example_list

def extend_no_dup(example_list, new_examples):
    """
    Adds each example in `new_examples`
    iff it has no duplicate in `example_list`
    @pre: - `example_list` must be a sorted list (with key == text).
          - `example_list` does not contain duplicates.
          - `new_examples` must be a sorted list (with key == text).
          - `new_examples` does not contain duplicates.
    @post: the returned list is sorted.
    """
    if len(new_examples) == 0:
        return example_list
    if len(example_list) == 0:
        return new_examples
    # TODO there might be a more optimized way to do that
    for ex in new_examples:
        example_list = add_example_no_dup(example_list, ex)
    return example_list


def sort_by_texts(example_list):
    """
    Returns a sorted list of examples (with key == text).
    @pre: - `example_list` contains no duplicates.
    """
    return sorted(example_list, key=lambda ex: ex.text)