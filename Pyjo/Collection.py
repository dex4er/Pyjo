# -*- coding: utf-8 -*-

"""
Pyjo.Collection - Collection
============================
::

    import Pyjo.Collection

    collection = Pyjo.Collection.new('just', 'works')
"""


import Pyjo.ByteStream


DEFAULT_CHARSET = 'utf-8'


class Pyjo_Collection(list):
    """::

        stream = Pyjo.Collection.new(1, 2, 3)

    Construct a new :mod:`Pyjo.TextStream` object.
    """
    def __new__(cls, *args):
        return super(Pyjo_Collection, cls).__new__(cls)

    def __init__(self, *args):
        self.extend(args)

    @classmethod
    def new(cls, *args):
        return Pyjo_Collection(*args)

    def flatten(self):
        def _flatten(array):
            for item in array:
                if isinstance(item, (list, tuple)):
                    for subitem in _flatten(item):
                        yield subitem
                else:
                    yield item

        return self.new(*_flatten(self))


def c(*args):
    """::

        stream = c(1, 2, 3)

    Construct a new :mod:`Pyjo.Collection` object.
    """
    return Pyjo_Collection(*args)


new = Pyjo_Collection.new
object = Pyjo_Collection  # @ReservedAssignment
