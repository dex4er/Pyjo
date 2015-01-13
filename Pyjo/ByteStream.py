# -*- coding: utf-8 -*-

"""
Pyjo.ByteStream - ByteStream
============================
::

    import Pyjo.ByteStream

    stream = Pyjo.ByteStream.new('foo_bar_baz')
"""


import Pyjo.TextStream

import sys


if sys.version_info >= (3, 0):
    base_object = bytes
else:
    base_object = str


DEFAULT_CHARSET = 'utf-8'


class Pyjo_ByteStream(base_object):
    """::

        stream = Pyjo.ByteStream.new('test123')

    Construct a new :mod:`Pyjo.ByteStream` object.
    """
    def __new__(cls, value, charset=DEFAULT_CHARSET):
        if sys.version_info >= (3, 0):
            if isinstance(value, bytes):
                return super(Pyjo_ByteStream, cls).__new__(cls, value)
            elif isinstance(value, str):
                return super(Pyjo_ByteStream, cls).__new__(cls, value, charset)
            else:
                return super(Pyjo_ByteStream, cls).__new__(cls, str(value), charset)
        else:
            if isinstance(value, unicode):
                return super(Pyjo_ByteStream, cls).__new__(cls, value.encode(charset))
            else:
                return super(Pyjo_ByteStream, cls).__new__(cls, value)

    def decode(self, charset=DEFAULT_CHARSET):
        return Pyjo.TextStream.new(super(Pyjo_ByteStream, self).decode(charset))

    @classmethod
    def new(cls, value, charset=DEFAULT_CHARSET):
        return Pyjo_ByteStream(value, charset)


def b(value, charset=DEFAULT_CHARSET):
    """::

        stream = b('test123')

    Construct a new :mod:`Pyjo.ByteStream` object.
    """
    return Pyjo_ByteStream(value, charset)


new = Pyjo_ByteStream.new
object = Pyjo_ByteStream  # @ReservedAssignment
