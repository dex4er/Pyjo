"""
Pyjo.Path
"""

import Pyjo.Base.String


# TODO stub
class Pyjo_Path(Pyjo.Base.String.object):

    def __init__(self, string=None):
        if string is None:
            self.string = ''
        else:
            self.string = string

    def to_string(self):
        return self.string


def new(*args, **kwargs):
    return Pyjo_Path(*args, **kwargs)

object = Pyjo_Path  # @ReservedAssignment
