"""
Module `chatette.parsing.line_count_file_wrapper`.
Contains a wrapper of `io.File` that counts on which line it is currently.
"""

import io


class LineCountFileWrapper(object):
    """
    A wrapper of `io.File` that keeps track of the line number it is reading.
    """
    
    def __init__(self, filepath, mode='r'):
        self.name = filepath
        self.f = io.open(filepath, mode)
        self.line_nb = 0

    def close(self):
        return self.f.close()
    def closed(self):
        return self.f.closed

    def readline(self):
        self.line_nb += 1
        return self.f.readline()

    # to allow using in 'with' statements 
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        self.close()

