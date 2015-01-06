# -*- coding: utf-8 -*-

"""
Pyjo.TextStream - TextStream
============================
::

    import Pyjo.TextStream

    stream = Pyjo.TextStream.new('foo_bar_baz')
"""


import Pyjo.ByteStream

import sys


if sys.version_info >= (3, 0):
    base_object = str
else:
    base_object = unicode


DEFAULT_CHARSET = 'utf-8'


class Pyjo_TextStream(base_object):
    """::

        stream = Pyjo.TextStream.new('test123')

    Construct a new :mod:`Pyjo.TextStream` object.
    """
    def __new__(cls, value, charset=DEFAULT_CHARSET):
        if sys.version_info >= (3, 0):
            if isinstance(value, bytes):
                return super(Pyjo_TextStream, cls).__new__(cls, value.decode(charset))
            else:
                return super(Pyjo_TextStream, cls).__new__(cls, str(value))
        else:
            if isinstance(value, unicode):
                return super(Pyjo_TextStream, cls).__new__(cls, value)
            elif isinstance(value, str):
                return super(Pyjo_TextStream, cls).__new__(cls, unicode(value).decode(charset))
            else:
                return super(Pyjo_TextStream, cls).__new__(cls, unicode(value))

    def encode(self, charset=DEFAULT_CHARSET):
        return Pyjo.ByteStream.new(super(Pyjo_TextStream, self).encode(charset))

    @classmethod
    def new(cls, value, charset=DEFAULT_CHARSET):
        return Pyjo_TextStream(value, charset)


def u(value, charset=DEFAULT_CHARSET):
    """::

        stream = u('test123')

    Construct a new :mod:`Pyjo.TextStream` object.
    """
    return Pyjo_TextStream(value, charset)


new = Pyjo_TextStream.new
object = Pyjo_TextStream  # @ReservedAssignment
