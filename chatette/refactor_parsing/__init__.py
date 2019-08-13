# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing`
Contains everything that is related to the management and parsing
of the template file(s).
The most important classes defined in this module are:
- Parser, which runs the whole parsing of template files
- Lexer, in charge of "lexing" the information present in those files
- InputFileMnaager, which manages the opening, closing and read of those files
"""
# TODO Add LineCountFileWrapper in here

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

from chatette.refactor_units.choice import Choice
from chatette.refactor_units.unit_reference import UnitReference


class IntermediateRepr(with_metaclass(ABCMeta, object)):
    corresponding_class = None
    def __init__(self):
        self.casegen = False
        self.randgen = False
        self.randgen_name = None
        self.randgen_percent = 50
    
    @abstractmethod
    def create_concrete(self):
        raise NotImplementedError()

class ChoiceRepr(IntermediateRepr):
    corresponding_class = Choice
    def __init__(self):
        super(ChoiceRepr, self).__init__()
        self.rules = []
    
    def create_concrete(self):
        return Choice("No name", self.rules)

class UnitRefRepr(object):
    corresponding_class = UnitReference
    def __init__(self):
        super(UnitRefRepr, self).__init__()
        self.type = None
        self.identifier = None
        self.variation = None
        self.arg_value = None
    
    def create_concrete(self):
        if self.type is None or self.identifier is None:  # Should never happen
            raise ValueError(
                "Tried to create a concrete unit reference without setting " + \
                "its identifier or type."
            )
        return self.__class__.corresponding_class(self.identifier, self.type)
