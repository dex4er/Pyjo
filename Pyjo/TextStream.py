# -*- coding: utf-8 -*-

"""
Pyjo.TextStream - TextStream
============================
::

    import Pyjo.TextStream

    stream = Pyjo.TextStream.new('foo_bar_baz')
"""


import Pyjo.ByteStream
import Pyjo.Util

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

    def html_unescape(self):
        """::

            stream = stream.html_unescape()

        Unescape all HTML entities in bytestream with :func:`Pyjo.Util.html_unescape`. ::

            b('&lt;html&gt;').html_unescape().url_escape().say()
        """
        return self.new(Pyjo.Util.html_unescape(self))

    def encode(self, charset=DEFAULT_CHARSET):
        """::

            stream = $stream->encode;
            stream = $stream->encode('iso-8859-1')

        Encode bytestream, defaults to ``utf-8``, and return new :mod:`Pyjo.ByteStream` object. ::

            stream.trim().quote().encode().say()
        """
        return Pyjo.ByteStream.new(super(Pyjo_TextStream, self).encode(charset))

    @classmethod
    def new(cls, value, charset=DEFAULT_CHARSET):
        return Pyjo_TextStream(value, charset)

    def say(self):
        print(self)


def u(value, charset=DEFAULT_CHARSET):
    """::

        stream = u('test123')

    Construct a new :mod:`Pyjo.TextStream` object.
    """
    return Pyjo_TextStream(value, charset)


new = Pyjo_TextStream.new
object = Pyjo_TextStream  # @ReservedAssignment
