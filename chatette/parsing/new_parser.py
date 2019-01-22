import os

from chatette.utils import print_DBG, print_warn
import chatette.parsing.parser_utils as pu
from chatette.parsing.tokenizer import Tokenizer


class Parser(object):
    """
    **This class is a refactor of the current parser**
    This class will parse the input file(s)
    and create an internal representation of its contents (as an AST).
    """
    
    def __init__(self, master_filename):
        self.tokenizer = Tokenizer(master_filename)

    def parse(self):
        for token_line in self.tokenizer.next_tokenized_line():
            print(self.tokenizer.get_file_information(), token_line)