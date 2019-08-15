# coding: utf-8
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

from chatette.refactor_units.modifiable.choice import Choice
from chatette.refactor_units.modifiable.unit_reference import UnitReference
from chatette.refactor_units.modifiable.definitions.alias import AliasDefinition
from chatette.refactor_units.modifiable.definitions.slot import SlotDefinition
from chatette.refactor_units.modifiable.definitions.intent import IntentDefinition


class ItemBuilder(with_metaclass(ABCMeta, object)):
    """
    An intermediate representation of generating items that are used by the
    parser. It is able to construct the corresponding item once it has
    all the required information.
    NOTE: This does not correspond to the *Builder* design pattern.
    """
    def __init__(self):
        self.casegen = False
        self.randgen = False
        self.randgen_name = None
        self.randgen_percent = 50
    
    def _check_information(self):
        if not self.randgen and self.randgen_name is not None:  # Should never happen
            raise ValueError(
                "There was a problem with some modifiers: detected " + \
                "a random generation modifier name but no " + \
                "random generation modifier."
            )
    
    @abstractmethod
    def create_concrete(self):
        raise NotImplementedError()

class ChoiceBuilder(ItemBuilder):
    def __init__(self):
        super(ChoiceBuilder, self).__init__()
        self.rules = []
    
    def create_concrete(self):
        self._check_information()
        return Choice("No name", self.rules)

class UnitRefBuilder(ItemBuilder):
    def __init__(self):
        super(UnitRefBuilder, self).__init__()
        self.type = None
        self.identifier = None
        self.variation = None
        self.arg_value = None
    
    def _check_information(self):
        super(UnitRefBuilder, self)._check_information()
        if self.type is None or self.identifier is None:  # Should never happen
            raise ValueError(
                "Tried to create a concrete unit reference without setting " + \
                "its identifier or type."
            )

    def create_concrete(self):
        self._check_information()
        return UnitReference(self.identifier, self.type)

class UnitDefBuilder(ItemBuilder):
    def __init__(self):
        super(UnitDefBuilder, self).__init__()
        self.identifier = None
        self.variation = None
        self.arg_name = None
    
    def _check_information(self):
        super(UnitDefBuilder, self)._check_information()
        if self.identifier is None:  # Should never happen
            raise ValueError(
                "Tried to create a concrete unit definition " + \
                "without setting its identifier."
            )

class AliasDefBuilder(UnitDefBuilder):
    def create_concrete(self):
        self._check_information()
        return AliasDefinition(self.identifier)
class SlotDefBuilder(UnitDefBuilder):
    def create_concrete(self):
        self._check_information()
        return SlotDefinition(self.identifier)
class IntentDefBuilder(UnitDefBuilder):
    def __init__(self):
        super(IntentDefBuilder, self).__init__()
        self.nb_training_ex = None
        self.nb_testing_ex = None
    
    def create_concrete(self):
        self._check_information()
        return IntentDefinition(
            self.identifier, self.nb_training_ex, self.nb_testing_ex
        )
