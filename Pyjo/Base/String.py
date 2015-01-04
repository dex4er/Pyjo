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

    def __add__(self, other):
        return str(self) + other

    def __bool__(self):
        return bool(self.to_str())

    def __bytes__(self):
        return bytes(self.to_str(), 'utf-8')

    def __complex__(self):
        return complex(self.to_str())

    def __contains__(self, other):
        return other in str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __float__(self):
        return float(self.to_str())

    def __ge__(self, other):
        return str(self) >= str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __hash__(self):
        return hash(self.to_str())

    def __hex__(self):
        return hex(int(self.to_str()))

    def __iadd__(self, other):
        self.parse(str(self) + other)
        return self

    def __imul__(self, other):
        self.parse(str(self) * other)
        return self

    def __int__(self):
        return int(self.to_str())

    def __le__(self, other):
        return str(self) <= str(other)

    def __long__(self):
        return long(self.to_str())

    def __lt__(self, other):
        return str(self) < str(other)

    def __mul__(self, other):
        return str(self) * other

    def __ne__(self, other):
        return str(self) != str(other)

    def __nonzero__(self):
        return bool(self.to_str())

    def __oct__(self):
        return oct(int(self.to_str()))

    def __radd__(self, other):
        return other + str(self)

    def __repr__(self):
        if self.__module__ == '__main__':
            return "{0}('{1}')".format(self.__class__.__name__, str(self))
        else:
            return "{0}.{1}('{2}')".format(self.__module__, self.__class__.__name__, str(self))

    def __str__(self):
        string = self.to_str()
        if string is None:
            string = 'None'
        return string


new = Pyjo_Base_String.new
object = Pyjo_Base_String  # @ReservedAssignment
