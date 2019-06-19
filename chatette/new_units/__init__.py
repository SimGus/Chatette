"""
Module `chatette.new_units`
Contains the defintion of units (i.e. definitions, rules and their contents)
that make up the Abstract Syntax Tree, and the logic associated with
the generation of examples.
"""


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
        return hash(self.text+str(self.entities))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
