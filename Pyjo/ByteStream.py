# -*- coding: utf-8 -*-

"""
Pyjo.ByteStream - ByteStream
============================
::

    import Pyjo.ByteStream

    # Manipulate bytestream
    stream = Pyjo.ByteStream.new('foo:bar:baz')
    print(stream.url_escape().decode('ascii'))

    # Use the alternative constructor
    from Pyjo.ByteStream import b
    bstream = b('foo:bar:baz').url_escape()

:mod:`Pyjo.ByteStream` is a container for bytestreams that provides a
more friendly API for many of the functions in :mod:`Pyjo.Util`.

It also inherits all attributes and methods from
either :class:`str` (Python 2.x) or :class:`bytes` (Python 3.x).

Classes
-------
"""

import Pyjo.TextStream
import Pyjo.Util

import sys


if sys.version_info >= (3, 0):
    base_object = bytes
else:
    base_object = str


DEFAULT_CHARSET = 'utf-8'


class Pyjo_ByteStream(base_object):
    """
    :mod:`Pyjo.ByteStream` inherits all attributes and methods from
    either :class:`str` (Python 2.x) or :class:`bytes` (Python 3.x)
    and implements the following new ones.
    """

    def __new__(cls, value=b'', charset=DEFAULT_CHARSET):
        return super(Pyjo_ByteStream, cls).__new__(cls, Pyjo.Util.b(value, charset))

    def __repr__(self):
        return "{0}.new({1})".format(self.__module__, super(Pyjo_ByteStream, self).__repr__())

    def decode(self, charset=DEFAULT_CHARSET):
        """::

            stream = stream.decode()
            stream = stream.decode('iso-8859-1')

        Decode bytestream, defaults to ``utf-8``, and return new :mod:`Pyjo.TextStream` object. ::

            stream.decode('UTF-16LE').unquote().trim().say()

        """
        return Pyjo.TextStream.new(super(Pyjo_ByteStream, self).decode(charset))

    @classmethod
    def new(cls, value=b'', charset=DEFAULT_CHARSET):
        """::

            stream = Pyjo.ByteStream.new('test123')

        Construct a new :mod:`Pyjo.ByteStream` object.
        """
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


def b(value=b'', charset=DEFAULT_CHARSET):
    """::

        stream = b('test123')

    Construct a new :mod:`Pyjo.ByteStream` object.
    """
    return Pyjo_ByteStream(value, charset)


new = Pyjo_ByteStream.new
object = Pyjo_ByteStream  # @ReservedAssignment
