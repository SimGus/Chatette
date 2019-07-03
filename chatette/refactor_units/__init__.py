#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module `chatette.refactor_units`
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
    
    def __repr__(self):
        return "<'"+self.text+"' "+str(self.entities)+'>'
    def __str__(self):
        return self.text + '\n\tEntities: ' + str(self.entities)

    def __hash__(self):
        return hash(self.text+str(self.entities.__hash__()))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    def is_dup(self, other):
        """
        Returns `True` if this example is a duplicate of `other`.
        A duplicate is an example with the same text.
        """
        return this.text == other.text
    
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

class Entity(object):
    """
    Represents an entity as it will be contained in examples
    (instances of `Example`).
    """
    def __init__(self, name, length, start_index=0, value=None):
        self.name = name  # name of the entity (not the associated text)
        self.value = value
        self._len = length
        self._start_index = start_index
    
    def __repr__(self):
        representation = "entity '" + self.name + "'"
        if self.value is not None:
            representation += ":'" + self.value + "'"
        return representation
    def __str__(self):
        return self.name + "@" + str(self._index) + "\t=>\t" + str(self.value)
    
    def __hash__(self):
        return hash(self.name +"@" + str(self._index) + ":" + str(self.value))
    
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
    @pre: `example_list` must be a sorted list (with key == text).
          `example_list` does not contain duplicates.
    @post: the returned list is sorted.
    """
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
            hi = i - 1
        else:  # current_text < new_example.text
            lo = i + 1
        i = int(floor((hi - lo)/2)) + lo

    # Add example if needed
    if not found:
        example_list.insert(i, new_example)
    # Remove example if needed
    elif len(example_list[i].entities) < len(new_example.entities):
        example_list[i] = new_example
    return example_list
