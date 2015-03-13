# -*- coding: utf-8 -*-

"""
Pyjo.BytesString - Bytes string
===============================
::

    import Pyjo.BytesString

    # Manipulate BytesString
    string = Pyjo.BytesString.new('foo:bar:baz')
    print(string.url_escape().decode('ascii'))

    # Use the alternative constructor
    from Pyjo.BytesString import b
    bstring = b('foo:bar:baz').url_escape()

:mod:`Pyjo.BytesString` is a container for BytesStrings that provides a
more friendly API for many of the functions in :mod:`Pyjo.Util`.

It also inherits all attributes and methods from
either :class:`str` (Python 2.x) or :class:`bytes` (Python 3.x).

Classes
-------
"""

import Pyjo.UnicodeString
import Pyjo.Util

import sys


if sys.version_info >= (3, 0):
    base_object = bytes
else:
    base_object = str


DEFAULT_CHARSET = 'utf-8'


class Pyjo_BytesString(base_object):
    """
    :mod:`Pyjo.BytesString` inherits all attributes and methods from
    either :class:`str` (Python 2.x) or :class:`bytes` (Python 3.x)
    and implements the following new ones.
    """

    def __new__(cls, value=b'', charset=DEFAULT_CHARSET):
        return super(Pyjo_BytesString, cls).__new__(cls, Pyjo.Util.b(value, charset))

    def __repr__(self):
        return "{0}.new({1})".format(self.__module__, super(Pyjo_BytesString, self).__repr__())

    def decode(self, charset=DEFAULT_CHARSET):
        """::

            string = string.decode()
            string = string.decode('iso-8859-1')

        Decode BytesString, defaults to ``utf-8``, and return new :mod:`Pyjo.UnicodeString` object. ::

            string.decode('UTF-16LE').unquote().trim().say()

        """
        return Pyjo.UnicodeString.new(super(Pyjo_BytesString, self).decode(charset))

    @classmethod
    def new(cls, value=b'', charset=DEFAULT_CHARSET):
        """::

            string = Pyjo.BytesString.new('test123')

        Construct a new :mod:`Pyjo.BytesString` object.
        """
        return Pyjo_BytesString(value, charset)

    def url_escape(self):
        """::

            string = string.url_escape()
            string = string.url_escape(br'^A-Za-z0-9\-._~')

        Percent encode all unsafe characters in BytesString with
        :func:`Pyjo.Util.url_escape`. ::

            b('foo bar baz').url_escape().decode().say()
        """
        return self.new(Pyjo.Util.url_escape(self))

    def url_unescape(self):
        """

            string = string.url_unescape()

        Decode percent encoded characters in BytesString with
        :func:`Pyjo.Util.url_unescape`. ::

            b('%3Chtml%3E').url_unescape().decode().xml_escape().say()
        """
        return self.new(Pyjo.Util.url_unescape(self))


def b(value=b'', charset=DEFAULT_CHARSET):
    """::

        string = b('test123')

    Construct a new :mod:`Pyjo.BytesString` object.
    """
    return Pyjo_BytesString(value, charset)


new = Pyjo_BytesString.new
object = Pyjo_BytesString  # @ReservedAssignment
