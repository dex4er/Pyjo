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
        """::

            stream = stream.decode()
            stream = stream.decode('iso-8859-1')

        Decode bytestream, defaults to ``utf-8``, and return new :mod:`Pyjo.TextStream` object. ::

            stream.decode('UTF-16LE').unquote().trim().say()

        """
        return Pyjo.TextStream.new(super(Pyjo_ByteStream, self).decode(charset))

    @classmethod
    def new(cls, value, charset=DEFAULT_CHARSET):
        return Pyjo_ByteStream(value, charset)

    def url_escape(self):
        """::

            stream = stream.url_escape()
            stream = stream.url_escape(br'^A-Za-z0-9\-._~')

        Percent encode all unsafe characters in bytestream with
        :func:`Pyjo.Util.url_escape`. ::

            b('foo bar baz').url_escape().decode().say()
        """
        return self.new(Pyjo.Util.url_escape(self))

    def url_unescape(self):
        """

            stream = stream.url_unescape()

        Decode percent encoded characters in bytestream with
        :func:`Pyjo.Util.url_unescape`. ::

            b('%3Chtml%3E').url_unescape().decode().xml_escape().say()
        """
        return self.new(Pyjo.Util.url_unescape(self))


def b(value, charset=DEFAULT_CHARSET):
    """::

        stream = b('test123')

    Construct a new :mod:`Pyjo.ByteStream` object.
    """
    return Pyjo_ByteStream(value, charset)


new = Pyjo_ByteStream.new
object = Pyjo_ByteStream  # @ReservedAssignment
