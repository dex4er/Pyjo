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
    def __new__(cls, value=[]):
        return super(Pyjo_Collection, cls).__new__(cls, value)

    def __repr__(self):
        return "{0}.new({1})".format(self.__module__, super(Pyjo_Collection, self).__repr__())

    def flatten(self):
        return self.new(_flatten(self))

    def join(self, string=u''):
        return Pyjo.TextStream.new(string.join(map(lambda s: Pyjo.Util.u(s), self)))

    def map(self, method, *args):
        """::

            new = collection.map(lambda a: ...)
            new = collection.map(method)
            new = collection.map(method, *args)

        Evaluate callback for, or call method on, each element in collection and
        create a new collection from the results. The element will be the first
        argument passed to the callback. ::

            # Longer version
            new = collection.map(lambda a: getattr(a, method)(*args), *args)

            # Append the word "pyjo" to all values
            pyjoified = collection.map(lambda a: a + 'pyjo')
        """
        if callable(method):
            return self.new(map(method, self))
        else:
            return self.new(map(lambda a: getattr(a, method)(*args), self))

    @classmethod
    def new(cls, value=[]):
        return Pyjo_Collection(value)

    def to_list(self):
        return list(self)

    def to_tuple(self):
        return tuple(self)


def c(value=[]):
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
