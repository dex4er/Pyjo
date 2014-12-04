"""
Pyjo.Base.String
"""


from Pyjo.Base import *

from Pyjo.Base import not_implemented


__all__ = ['Pyjo_Base_String']


class Pyjo_Base_String(Pyjo_Base):

    @not_implemented
    def to_string(self):
        pass

    @not_implemented
    def parse(self):
        pass

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        if self.__module__ == '__main__':
            return "{0}('{1}')".format(self.__class__.__name__, str(self))
        else:
            return "{0}.{1}('{2}')".format(self.__module__, self.__class__.__name__, str(self))

    def __bytes__(self):
        return bytes(self.to_string(), 'utf-8')

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
        return bool(self.to_string())

    def __bool__(self):
        return bool(self.to_string())

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


def new(*args, **kwargs):
    return Pyjo_Base_Stream(*args, **kwargs)
