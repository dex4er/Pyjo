# -*- coding: utf-8 -*-

"""
Pyjo.Collection - Collection
============================
::

    import Pyjo.Collection

    collection = Pyjo.Collection.new(['just', 'works'])
"""


import Pyjo.TextStream


DEFAULT_CHARSET = 'utf-8'


class Pyjo_Collection(list):
    """::

        stream = Pyjo.Collection.new([1, 2, 3])

    Construct a new :mod:`Pyjo.Collection` object.
    """
    def __new__(cls, value):
        return super(Pyjo_Collection, cls).__new__(cls)

    @classmethod
    def new(cls, value):
        return Pyjo_Collection(value)

    def flatten(self):
        return self.new(_flatten(self))

    def join(self, string=u''):
        return Pyjo.TextStream.new(string.join(map(lambda s: Pyjo.Util.u(s), self)))


def c(value):
    """::

        collection = c([1, 2, 3])

    Construct a new :mod:`Pyjo.Collection` object.
    """
    return Pyjo_Collection(value)


def _flatten(array):
    for item in array:
        if isinstance(item, (list, tuple)):
            for subitem in _flatten(item):
                yield subitem
        else:
            yield item


new = Pyjo_Collection.new
object = Pyjo_Collection  # @ReservedAssignment
