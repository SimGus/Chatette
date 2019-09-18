# coding: utf-8

from warnings import warn

from chatette.utils import Singleton, print_warn, cast_to_unicode
from chatette.parsing.utils import \
     OLD_COMMENT_SYM, COMMENT_SYM, \
     OLD_CHOICE_START, OLD_CHOICE_END, CHOICE_START, CHOICE_END


class Deprecations(Singleton):
     _instance = None
     def __init__(self):
          self._old_comment_warned = False
          self._old_choice_warned = False
     
     def warn_old_comment(self, filename=None, line_nb=None, line=None):
          """
          Warns the user on stderr that one of their files contains semicolons
          comments (which are a deprecated way of making comments).
          Rather use '//' comments instead of ';' comments.
          """
          if not self._old_comment_warned:
               self._old_comment_warned = True
               message = \
                    "Comments starting with a semi-colon '" + \
                    OLD_COMMENT_SYM + "' are now deprecated. " + \
                    "Please use the new double slash '" + COMMENT_SYM + \
                    "' syntax instead."
               if filename is not None:
                    message += \
                         "\nThis syntax was found in file '" + \
                         cast_to_unicode(filename) + "'"
                    if line_nb is not None and line is not None:
                         message += \
                              " at line " + str(line_nb) + ": '" + \
                              str(line).strip() + "'"
                    message += '.'
               elif line_nb is not None and line is not None:
                    message += \
                         "\nThis syntax was found at line " + str(line_nb) + \
                         ": '" + str(line).strip() + "'."
               warn(message, DeprecationWarning)
               print_warn(message)

     def warn_old_choice(self, filename=None, line_nb=None, line=None):
          """
          Warns the user on stderr that one of their files contains semicolons
          comments (which are a deprecated way of making comments).
          Rather use '//' comments instead of ';' comments.
          """
          if not self._old_choice_warned:
               self._old_choice_warned = True
               message = \
                    "Choices starting with '" + OLD_CHOICE_START + \
                    "' and ending with '" + OLD_CHOICE_END + \
                    "' are now deprecated. Please use the new syntax that " + \
                    "starts with '" + CHOICE_START + "' and ends with '" + \
                    CHOICE_END + "' instead."
               if filename is not None:
                    message += \
                         "\nThis syntax was found in file '" + \
                         cast_to_unicode(filename) + "'"
                    if line_nb is not None and line is not None:
                         message += \
                              " at line " + str(line_nb) + ": '" + \
                              str(line).strip() + "'"
                    message += '.'
               elif line_nb is not None and line is not None:
                    message += \
                         "\nThis syntax was found at line " + str(line_nb) + \
                         ": '" + str(line).strip() + "'."
               warn(message, DeprecationWarning)
               print_warn(message)
