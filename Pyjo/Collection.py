# -*- coding: utf-8 -*-

"""
Pyjo.Collection - Collection
============================
::

    import Pyjo.Collection

    collection = Pyjo.Collection.new(['just', 'works'])
"""


import Pyjo.TextStream

from Pyjo.Regexp import m


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

    def each(self, cb=None):
        """::

            elements = collection.each()
            collection = collection.each(lambda e, num: ...)

        Evaluate callback for each element in collection or return all elements as a
        list if none has been provided. The element will be the first argument passed
        to the callback. ::

            # Make a numbered list
            collection.each(lambda e, num:
                print("{0}: {1}".format(e, num)
            )
        """
        if cb is None:
            return self.to_list()
        else:
            num = 1
            for i in self:
                cb(i, num)
                num += 1
            return self

    def first(self, cb=None, flags=''):
        """::

            first = collection.first()
            first = collection.first(r'pattern', 'flags')
            first = collection.first(lambda i: ...)

        Evaluate regular expression or callback for each element in collection and
        return the first one that matched the regular expression, or for which the
        callback returned true. The element will be the first argument passed to the
        callback. ::

            # Find first value that contains the word "mojo"
            interesting = collection.first('pyjo', 'i')

            # Find first value that is greater than 5
            greater = collection.first(lambda i: i > 5)
        """
        if cb is None:
            return self[0]
        elif callable(cb):
            for i in self:
                if cb(i):
                    return i
        else:
            for i in self:
                if i == m(cb, flags):
                    return i
        return

    def flatten(self):
        """::

            my $new = $collection->flatten;

        Flatten nested collections/lists/tuples recursively and create a new collection with
        all elements. ::

            # "1, 2, 3, 4, 5, 6, 7"
            Pyjo.Collection.new([1, [2, [3, 4], 5, [6]], 7]).flatten().join(', ').say()
        """
        return self.new(_flatten(self))

    def grep(self, cb, flags=''):
        """::

            new = collection.grep(r'pattern', 'flags')
            new = collection.grep(lambda i: ...)

        Evaluate regular expression or callback for each element in collection and
        create a new collection with all elements that matched the regular expression,
        or for which the callback returned true. The element will be the first
        argument passed to the callback.

            # Find all values that contain the word "mojo"
            interesting = collection.grep('mojo', 'i')

            # Find all values that are greater than 5
            greater = collection.grep(lambda i: i > 5)
        """
        if callable(cb):
            return self.new(filter(lambda i: cb(i), self))
        else:
            return self.new(filter(lambda i: i == m(cb, flags), self))

    def item(self, offset):
        """::

            item = collection.item(0)

        Return element from collection. ::

            # the same as
            item = collection[0]
        """
        return self[offset]

    def join(self, string=u''):
        """::

            stream = collection.join()
            stream = collection.join("\\n")

        Turn collection into :mod:`Pyjo.ByteStream`. ::

            # Join all values with commas
            collection.join(', ').say()
        """
        return Pyjo.TextStream.new(string.join(map(lambda s: Pyjo.Util.u(s), self)))

    def map(self, attribute, *args):
        """::

            new = collection.map(lambda a: ...)
            new = collection.map(attribute)
            new = collection.map(attribute, value)
            new = collection.map(method)
            new = collection.map(method, *args)

        Evaluate callback for, or get/set attribute from,
        or call method on, each element in collection and
        create a new collection from the results. The element will be the first
        argument passed to the callback. ::

            # Longer version for attribute
            new = collection.map(lambda a: getattr(a, attribute))
            new = collection.map(lambda a: setattr(a, attribute, value))

            # Longer version for method
            new = collection.map(lambda a: getattr(a, method)(*args))

            # Append the word "pyjo" to all values
            pyjoified = collection.map(lambda a: a + 'pyjo')
        """
        if callable(attribute):
            return self.new(map(attribute, self))
        else:
            return self.new(
                map(lambda a:
                    getattr(a, attribute)(*args) if callable(getattr(a, attribute))
                    else getattr(a, attribute, setattr(a, attribute, args[0])) if args
                    else getattr(a, attribute),
                    self))

    @classmethod
    def new(cls, value=[]):
        return Pyjo_Collection(value)

    def size(self):
        """::

            size = collection.size()

        Number of elements in collection.
        """
        return len(self)

    def to_dict(self):
        """::

            d = params.to_dict()

        Turn collection of pairs of key and value into a :class:`dict`. ::

            # {'b': 2, 'a': 1, 'c': 3}
            Pyjo.Collection.new([('a', 1), ('b', 2), ('c', 3)]).to_dict()
        """
        return list(self)

    def to_iter(self):
        """::

            i = params.to_iter()

        Turn collection into a :class:`iter` iterator. ::

            for i in Pyjo.Collection.new([1, 2, 3]).to_iter():
                print(i)
        """
        return list(self)

    def to_list(self):
        """::

            l = params.to_list()

        Turn collection into a :class:`list`. ::

            # [1, 2, 3]
            Pyjo.Collection.new([1, 2, 3]).to_list()
        """
        return list(self)

    def to_set(self):
        """::

            s = params.to_set()

        Turn collection into a :class:`set`. ::

            # {1, 2, 3}
            Pyjo.Collection.new([1, 2, 3]).to_set()
        """
        return set(self)

    def to_tuple(self):
        """::

            t = params.to_tuple()

        Turn collection into a :class:`tuple`. ::

            # (1, 2, 3)
            Pyjo.Collection.new([1, 2, 3]).to_tuple()
        """
        return tuple(self)

    def zip(self, list2):
        """::

            new = collection.zip([1, 2, 3])

        Agregates elements from collection and iterable and returns new
        collection of pairs. ::

            # [('a', 1), ('b', 2), ('c', 3)]
            Pyjo.Collection.new(['a', 'b', 'c']).zip([1, 2, 3])

        """
        return Pyjo.Collection.new(zip(self, list2))


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
