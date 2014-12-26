"""
Pyjo.Base.String
"""


import Pyjo.Base

from Pyjo.Util import not_implemented


class Pyjo_Base_String(Pyjo.Base.object):

    @not_implemented
    def to_str(self):
        pass

    @not_implemented
    def parse(self):
        pass

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        if self.__module__ == '__main__':
            return "{0}('{1}')".format(self.__class__.__name__, str(self))
        else:
            return "{0}.{1}('{2}')".format(self.__module__, self.__class__.__name__, str(self))

    def __bytes__(self):
        return bytes(self.to_str(), 'utf-8')

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __nonzero__(self):
        return bool(self.to_str())

    def __bool__(self):
        return bool(self.to_str())

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def __iadd__(self, other):
        self.parse(str(self) + other)
        return self

    def __mul__(self, other):
        return str(self) * other

    def __imul__(self, other):
        self.parse(str(self) * other)
        return self

    def __contains__(self, other):
        return other in str(self)


new = Pyjo_Base_String.new
object = Pyjo_Base_String  # @ReservedAssignment
