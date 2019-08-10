# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.lexing_rule`
Contains the class that represents a lexing rule, which is
in charge of checking if the rule it represents matces the input,
transforms it to lexical tokens (simply called tokens in the code) and
formulates the error if required. Therefore, each instance of such a class is
stateful.
"""

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

from chatette.refactor_parsing.input_file_manager import InputFileManager


class LexingRule(with_metaclass(ABCMeta, object)):
    """
    Superclass for all lexing rules.
    Child classes each represent a concrete lexing rule (each instance keeping
    a state) and whose purpose will be to:
    - check whether the provided text matches the rule it represents
    - produce the sequence of lexical toekns if it matches
    - formulate the error and communicate it to the user if asked
    """
    _empty_match_allowed = False
    def __init__(self, text, start_index):
        self._text = text

        self._start_index = start_index
        self._next_index = start_index
        self._furthest_matched_index = start_index  # inclusive  # TODO keep this up-to-date
        self._tokens = []
        
        self._matched = None
        self.error_msg = None

    
    def matches(self, **kwargs):
        """
        Applies the rule to `self._text`
        and returns `True` if the rule could be applied successfully.
        `kwargs` will be passed to the subsequent call to `self._apply_strategy`.
        @post: `self.get_lexical_tokens()` will return valid tokens
               iff this method returned `True`.
        """
        print("Trying to match: " + self.__class__.__name__ + " on '" + self._text[self._start_index:] + "'")
        if self._matched is None:
            if self._start_index >= len(self._text):
                if self.__class__._empty_match_allowed:
                    self._matched = True
                else:
                    self._matched = False
                    self.error_msg = \
                        "Matching of rule '" + self.__class__.__name__ + "' " + \
                        "failed. Didn't expect an end of line there."
            else:
                self._matched = self._apply_strategy(**kwargs)
                self._furthest_matched_index = self._next_index - 1
            # TODO TMP DEBUG
            if self._matched:
                print("Matched: " + self.__class__.__name__ + " => " + str(self._tokens))
            else:
                print("Not matched: " + self.__class__.__name__)
        return self._matched
    @abstractmethod
    def _apply_strategy(self, **kwargs):
        """
        Strategy to apply the rule to the text `self._text`.
        Implements the design pattern "Strategy method".
        Returns `True` iff the rule could be applied successfully.
        If the rule doesn't match, `self.error_msg` should be updated
        accordingly.
        `kwargs` can be used to pass arguments that are specific to
        the current strategy.
        After this method was called, the following variables should be
        up-to-date:
        - if it matched: `self._tokens`, `self._next_index`,
                         `self._furthest_matched_index`
        - if it didn't match: `self._furthest_matched_index`, `self.error_msg`
        """
        # TODO keep `self._furthest_matched_index` up-to-date
        raise NotImplementedError()
    
    # Helpers for matching rules
    def _try_to_match_rule(self, rule_class, index=None):
        """
        Tries to match the rule represented by `rule_class`
        and updates `self._tokens` and `self._next_index` if the rule could be
        applied. If the rule couldn't be applied, `self.error_msg` is updated.
        `rule_class` is a subclass of `LexingRule`; `index` is an index in the
        text `self._text`.
        @returns: `True` iff the rule could be applied successfully.
        """
        if index is None:
            index = self._next_index
        rule = rule_class(self._text, index)
        if rule.matches():
            self._tokens.extend(rule.get_lexical_tokens())
            self._next_index = rule.get_next_index_to_match()
            return True
        else:
            self.error_msg = rule.error_msg
            return False

    def _match_one_of(self, rule_classes, index=None, **kwargs):
        """
        Finds which of the rules in `rule_classes` matches the text starting at
        index `index`.
        Try rules in order of appearance in `rule_classes`.
        `rule_classes` is a list of class of rules.
        Returns `True` iff one of the rules could apply.
        `kwargs` will be passed down to the subsequent `_matches`
        @pre: `rule_classes` contains at least one element.
        @post:
            - if a rule matched, `self._tokens` and `self._next_index`
              are updated.
            - if no rule matched, `self._matched` and `self.error_msg` are
              updated.
        @raises: `ValueError` if `rule_classes` does not contain any element.
        """
        if len(rule_classes) == 0:
            raise ValueError(
                "Lexer tried to apply no rule at all " + \
                "during application of rule '" + self.__class__.__name__ + \
                "'."
            )
        if index is None:
            index = self._next_index
        
        best_failed_rule = None
        longest_match_size = None
        for rule_class in rule_classes:
            rule = rule_class(self._text, index)
            if rule.matches(**kwargs):
                self._tokens.extend(rule.get_lexical_tokens())
                self._next_index = rule.get_next_index_to_match()
                return True
            else:
                match_size = rule.get_next_index_to_match() - index
                print("match size for " + rule.__class__.__name__ + " is: " + str(match_size))
                if best_failed_rule is None or match_size > longest_match_size:
                    best_failed_rule = rule
                    longest_match_size = match_size

        # No rule matched
        self._matched = False
        if longest_match_size == 0:
            self.error_msg = \
                "Invalid token. Expected either of the following rules: '" + \
                "', '".join([c.__name__ for c in rule_classes]) + "'."
        else:
            self.error_msg = best_failed_rule.error_msg
        return False
    
    def _match_any_order(self, rule_classes, index=None):
        """
        Matches as many rules as possible from `rule_classes` and this in any
        order, but each rule can be matched only once.
        If `None` is present in `rule_classes`, it is allowed to match 0 rules.
        Returns `True` if at least one rule matched (or 0 if allowed).
        `rule_classes` is a list of class of rules.
        @pre: `rule_classes` contains at least one element.
        @post:
            - if at least one rule matched, `self._tokens` and
              `self._next_index` are updated.
            - if no rule matched and at least 1 must be matched,
              `self._matched` and `self.error_msg` are updated.
            - if no rule matched and 0 rules were allowed to be matched,
              simply returns `False`. `self._matched` and `self.error_msg` are
              NOT updated.
        @raises: `ValueError` if `rule_classes` does not contain any element.
        """
        if len(rule_classes) == 0:
            raise ValueError(
                "Lexer tried to apply no rule at all " + \
                "during application of rule '" + self.__class__.__name__ + \
                "'."
            )
        if index is None:
            index = self._next_index
        no_match_allowed = False
        matched_some_rule = False
        
        remaining_rules = list(rule_classes)
        i = 0
        best_failed_rule = None
        longest_match_size = None
        while True:
            if i >= len(remaining_rules):
                break
            if remaining_rules[i] is None:
                no_match_allowed = True
                remaining_rules.remove(None)
                i = 0
            else:
                rule = (remaining_rules[i])(self._text, index)
                if rule.matches():
                    matched_some_rule = True
                    self._tokens.extend(self.get_lexical_tokens())
                    self._next_index = self.get_next_index_to_match()
                    index = self._next_index
                    remaining_rules.remove(remaining_rules[i])
                else:
                    i += 1
                    match_size = rule.get_next_index_to_match() - index
                    if best_failed_rule is None or match_size > longest_match_size:
                        best_failed_rule = rule
                        longest_match_size = match_size
        if matched_some_rule:
            return True
        if no_match_allowed:
            return True
        # No rule matched and no match is not allowed
        self._matched = False
        if longest_match_size == 0:
            self.error_msg = \
                "Invalid token. Expected either of the following rules: '" + \
                "', '".join([c.__name__ for c in rule_classes]) + "'."
        else:
            self.error_msg = best_failed_rule.error_msg
        return False

    
    # Getters
    def get_lexical_tokens(self):
        """
        Returns the lexical tokens after th rule was successfully applied
        using `self.matches()`.
        If this method is called before the rule was applied,
        the rule will be applied, but a `ValueError` may be raised in case
        the rule doesn't match the text.
        @returns: a list of `LexicalToken`s
        """
        if self._matched is None:
            self.matches()
        if not self._matched:
            raise ValueError(
                "Asked for the lexical tokens of a rule that did not " + \
                "match: '" + self.__class__.__name__ + "'."
            )
        return self._tokens
    def get_next_index_to_match(self):
        """
        Returns the next index in `self._text` that corresponds to
        the rule next in line. This index may correspond to the end of the text
        if the current rule covered the whole text or to the same index as
        `self._start_index` if the rule didn't match anything at all.
        @returns: an integer index
        """
        if self._matched is None:
            self.matches()
        return self._next_index
    

    def print_error(self):
        """
        If the corresponding rule didn't match,
        prints the relevant error so the user is aware of what the lexing
        problem was.
        """
        if self._matched is None:
            raise ValueError(
                "Tried to print an error for rule '" + self.__class__.__name__ + \
                "' before it was applied."
            )
        if self._matched:
            raise ValueError(
                "Tried to print an error for rule '" + self.__class__.__name__ + \
                "' when no error occurred."
            )
        if self.error_msg is None:
            raise ValueError(
                "No error to print for rule '" + self.__class__.__name__ + \
                "'."
            )
        InputFileManager.get_or_create() \
            .syntax_error(self.error_msg, self._next_index)
