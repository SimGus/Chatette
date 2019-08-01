# -*- coding: utf-8 -*-
"""
Module `chatette.refactor_parsing.lexing.lexing_rule`
Contains the class that represent a lexing rule
in charge of checking if the rule it represents matches the input,
transforms it to labelled tokens and formulates the error if needed.
Therefore, each instance is stateful.
"""

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

from chatette.refactor_parsing.input_file_manager import InputFileManager


class  LexingRule(with_metaclass(ABCMeta, object)):
    """
    Superclass for all lexing rules.
    Child-classes each represent a lexing rule (each instance keeping a state)
    and whose charge will be to:
    - check whether the provided text matches the rule it represents
    - produce the sequence of labelled tokens if it matches
    - formulate the error and communicate it to the user if asked
    """
    def __init__(self, text, start_index):
        self._file_manager = InputFileManager.get_or_create()
        self._text = text
        self._index = start_index
        self._next_index = None

        self._labelled_tokens = None
        self._matched = None
        self._match_length = None

        self.error_msg = None

        self._failed_child_rule = None
    
    @abstractmethod
    def matches(self):
        """
        Applies the rule to `self._text`
        and returns `True` if the rule could be applied correctly.
        @post: `self.get_labelled_tokens()` will return valid labelled tokens
               iff this method returned `True`.
        Implements the design pattern "Strategy method".
        """
        raise NotImplementedError()
    

    def get_labelled_tokens(self):
        """
        Returns the labelled tokens
        after the has been applied using `self.matches()`.
        If this method is called before the rule was applied,
        this could raise a `ValueError` in case the rule doesn't match.
        @returns: a list of `LabelledToken`s
        """
        if self._matched is None:
            self.matches()
        if not self._matched:
            raise ValueError(
                "Rule '" + self.__class__.__name__ + \
                "' did not match the provided text: '" + self._text + "'."
            )
        return self._labelled_tokens
    def get_next_index(self):
        """
        Returns the next index in `self._text` that corresponds to
        the rule next in line. This index may correspond to the end of the text
        if the current rule covered the whole text.
        @returns: an integer index
        """
        if self._matched is None:
            self.matches()
        if not self._matched:
            raise ValueError(
                "Rule '" + self.__class__.__name__ + \
                "' did not match the provided text: '" + self._text + "'."
            )
        return self._next_index


    def print_error(self):
        """
        If the corresponding rule didn't match,
        prints the relevant error so the user is aware of what the lexing
        problem was.
        """
        if self._matched is None:
            raise ValueError(
                "Tried to print an error for a rule that wasn't applied yet."
            )
        if self._matched:
            raise ValueError(
                "Tried to print an error for a rule that matched."
            )
        self._print_error()
    # @abstractmethod
    # def _print_error(self):
    #     """Concrete method to print the error of a rule that didn't match."""
    #     raise NotImplementedError()
    def _print_error(self):
        # TODO TMP
        self._file_manager.syntax_error(
            "Rule '" + self.__class__.__name__ + "' didn't match."
        )
