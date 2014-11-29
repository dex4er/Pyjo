"""
Pyjo.Path
"""

from Pyjo.Base import *


__all__ = ['Pyjo_Path']


# TODO stub
class Pyjo_Path(Pyjo_Base):

    def __init__(self, string=None):
        if string is None:
            self.string = ''
        else:
            self.string = string

    def to_string(self):
        return self.string

    __str__ = to_string
