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


new = Pyjo_Path.new
object = Pyjo_Path  # @ReservedAssignment
