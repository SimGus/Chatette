"""
Module `chatette.parsing.old_tokenizer`
Contains the tokenizer used by the old parser (Chatette <= v1.3.2).
"""

from chatette.utils import print_warn
import chatette.parsing.old_parser_utils as pu

class Tokenizer(object):
    def tokenize(self, text, line_nb=None, in_file_name=None):
        """Splits a string in a list of tokens (as strings)"""
        tokens = []
        current = ""

        escaped = False
        inside_choice = False
        for c in text:
            # Manage escapement
            if escaped:
                current += c
                escaped = False
                continue
            # elif c == pu.COMMENT_SYM_DEPRECATED:
            #     break
            elif inside_choice:
                if c == pu.CHOICE_CLOSE_SYM:
                    tokens.append(current + c)
                    current = ""
                    inside_choice = False
                else:
                    current += c
            elif c == pu.ESCAPE_SYM:
                escaped = True
                current += c
            elif c.isspace():
                if not pu.is_unit_start(current) and not pu.is_choice(current):  # End of word
                    if current != "":
                        tokens.append(current)
                    tokens.append(' ')
                    current = ""
                elif current == "" and \
                        len(tokens) > 0 and tokens[-1] == ' ':
                    continue  # Double space in-between words
                else:
                    current += c
            elif c == pu.UNIT_CLOSE_SYM:
                if pu.is_unit_start(current):
                    tokens.append(current + c)
                    current = ""
                else:
                    print_warn("Inconsistent use of the unit close symbol (" +
                                pu.UNIT_CLOSE_SYM + ") at line " + str(line_nb) +
                                " of file '" + in_file_name +
                                "'. Consider escaping them if they are " +
                                "not supposed to close a unit.\nThe generation will " +
                                "however continue, considering it as a normal character.")
                    current += c
            elif c == pu.CHOICE_CLOSE_SYM:
                print_warn("Inconsistent use of the choice close symbol (" +
                            pu.CHOICE_CLOSE_SYM + ") at line " + str(line_nb) +
                            " of file '" + in_file_name +
                            "'. Consider escaping them if they are " +
                            "not supposed to close a unit.\nThe generation will " +
                            "however continue, considering it as a normal character.")
                current += c
            elif c == pu.CHOICE_OPEN_SYM:
                if current != "":
                    tokens.append(current)
                inside_choice = True
                current = c
            elif pu.is_start_unit_sym(c) and current != pu.ALIAS_SYM and \
                    current != pu.SLOT_SYM and current != pu.INTENT_SYM:
                if current != "":
                    tokens.append(current)
                current = c
            else:  # Any other character
                current += c
        if current != "":
            tokens.append(current)
        return tokens
