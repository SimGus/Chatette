# coding: utf-8
"""
Module `chatette.parsing.lexing.rule_arg_decl`
Contains the definition of the class that represents the lexing rule
to tokenize the declaration of an argument in a unit declaration.
"""

from chatette.parsing.lexing.lexing_rule import LexingRule
from chatette.parsing.lexing import LexicalToken, TerminalType
from chatette.parsing.utils import \
    ARG_SYM, ARG_LIST_START, ARG_LIST_END, ARG_LIST_SEP, extract_identifier


class RuleArgDecl(LexingRule):
    def _apply_strategy(self, **kwargs):
        if not self._text.startswith(ARG_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected an argument declaration there " + \
                "(starting with '" + ARG_SYM + "')."
            return False
        self._next_index += 1
        self._update_furthest_matched_index()
        self._tokens.append(
            LexicalToken(TerminalType.arg_marker, ARG_SYM)
        )
        
        if not self._text.startswith(ARG_LIST_START, self._next_index):
            arg_name = extract_identifier(self._text, self._next_index)
            if arg_name is None:
                self.error_msg = \
                    "Didn't expect the line to end there. Expected an argument name."
                return False
            elif len(arg_name) == 0:
                self.error_msg = \
                    "Couldn't extract the argument name. Arguments must have a name."
                return False
            self._next_index += len(arg_name)
            self._update_furthest_matched_index()
            self._tokens.append(LexicalToken(TerminalType.arg_name, arg_name))
        else:
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.arg_start, ARG_LIST_START)
            )
            print("found ", ARG_LIST_START)

            while True:
                # TODO extract identifier should be done in a better way
                arg_name = extract_identifier(self._text, self._next_index)
                print("identifier: ", str(arg_name))
                if arg_name is None:
                    break
                self._next_index += len(arg_name)
                self._update_furthest_matched_index()
                self._tokens.append(
                    LexicalToken(TerminalType.arg_name, arg_name)
                )
                if not self._text.startswith(ARG_LIST_SEP):
                    break
                print("found ", ARG_LIST_SEP)
                self._next_index += 1
                self._update_furthest_matched_index()
                self._tokens.append(
                    LexicalToken(TerminalType.separator, ARG_LIST_SEP)
                )
            
            if not self._text.startswith(ARG_LIST_END):
                self.error_msg = \
                    "Missing closing parenthesis for argument list."
                return False
            print("found ", ARG_LIST_END)
            self._next_index += 1
            self._update_furthest_matched_index()
            self._tokens.append(
                LexicalToken(TerminalType.arg_end, ARG_LIST_END)
            )

        return True
