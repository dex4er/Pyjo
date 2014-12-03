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

    def __str__(self):
        return self.to_string()

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
