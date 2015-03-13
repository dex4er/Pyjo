# -*- coding: utf-8 -*-

"""
Pyjo.UnicodeString - Unicode string
===================================
::

    import Pyjo.UnicodeString

    # Manipulate UnicodeString
    string = Pyjo.UnicodeString.new('foo_bar_baz')
    print(string.camelize())

    # Chain methods
    string = Pyjo.UnicodeString.new('foo_bar_baz').quote()
    string = string.unquote().encode('utf-8').b64_encode('')
    print(string.decode('ascii'))

    # Use the alternative constructor
    from Pyjo.UnicodeString import u
    my $string = u('foobarbaz').camelize('').say()

:mod:`Pyjo.UnicodeString` is a container for UnicodeStrings that provides a
more friendly API for many of the functions in :mod:`Pyjo.Util`.

It also inherits all attributes and methods from
either :class:`unicode` (Python 2.x) or :class:`str` (Python 3.x).

Classes
-------
"""

from __future__ import print_function

import Pyjo.BytesString
import Pyjo.Util

import sys


if sys.version_info >= (3, 0):
    base_object = str
else:
    base_object = unicode


DEFAULT_CHARSET = 'utf-8'


class Pyjo_UnicodeString(base_object):
    """
    :mod:`Pyjo.UnicodeString` inherits all attributes and methods from
    either :class:`unicode` (Python 2.x) or :class:`str` (Python 3.x)
    and implements the following new ones.
    """

    def __new__(cls, value=u'', charset=DEFAULT_CHARSET):
        return super(Pyjo_UnicodeString, cls).__new__(cls, Pyjo.Util.u(value, charset))

    def __repr__(self):
        return "{0}.new({1})".format(self.__module__, super(Pyjo_UnicodeString, self).__repr__())

    def html_unescape(self):
        """::

            string = string.html_unescape()

        Unescape all HTML entities in UnicodeString with :func:`Pyjo.Util.html_unescape`. ::

            b('&lt;html&gt;').html_unescape().url_escape().say()
        """
        return self.new(Pyjo.Util.html_unescape(self))

    def encode(self, charset=DEFAULT_CHARSET):
        """::

            string = string.encode()
            string = string.encode('iso-8859-1')

        Encode UnicodeString, defaults to ``utf-8``, and return new :mod:`Pyjo.BytesString` object. ::

            string.trim().quote().encode().say()
        """
        return Pyjo.BytesString.new(super(Pyjo_UnicodeString, self).encode(charset))

    @classmethod
    def new(cls, value=u'', charset=DEFAULT_CHARSET):
        """::

            string = Pyjo.UnicodeString.new('test123')

        Construct a new :mod:`Pyjo.UnicodeString` object.
        """
        return Pyjo_UnicodeString(value, charset)

    def say(self, **kwargs):
        """::

            string = string.say()
            string = string.say(file=sys.stderr, end='', flush=True)

        Print UnicodeString to handle and append a newline, defaults to :attr:`sys.stdout`.
        """
        if 'flush' in kwargs and sys.version_info < (3, 0):
            flush = kwargs.pop('flush')
        else:
            flush = False
        print(self.to_str(), **kwargs)
        if flush:
            f = kwargs.get('file', sys.stdout)
            f.flush()
        return self

    def to_bytes(self, charset=DEFAULT_CHARSET):
        """::

            bstring = string.to_bytes()
            bstring = string.to_bytes(charset)

        Turn UnicodeString into a bytes string.
        """
        return Pyjo.Util.b(self, charset)

    def to_str(self, charset=DEFAULT_CHARSET):
        """::

            string = string.to_str()

        Turn UnicodeString into a string:
        on Python 2.x into bytes string, on Python 3.x into unicode string.
        """
        if sys.version_info >= (3, 0):
            return self.to_unicode(charset)
        else:
            return self.to_bytes(charset)

    def to_unicode(self, charset=DEFAULT_CHARSET):
        """::

            ustring = string.to_unicode()
            ustring = string.to_unicode(charset)

        Turn UnicodeString into an unicode string.
        """
        return Pyjo.Util.u(self, charset)

    def trim(self):
        """::

            string = string.trim()

        Trim whitespace characters from both ends of bytestring with :func:`Pyjo.Util.trim`.
        """
        return self.new(Pyjo.Util.trim(self))

    def xml_escape(self):
        """::

            string = string.xml_escape()

        Escape only the characters ``&``, ``<``, ``>``, ``"`` and ``'`` in
        UnicodeString with :func:`Pyjo.Util.xml_escape`.
        """
        return self.new(Pyjo.Util.xml_escape(self))


def u(value=u'', charset=DEFAULT_CHARSET):
    """::

        string = u('test123')

    Construct a new :mod:`Pyjo.UnicodeString` object.
    """
    return Pyjo_UnicodeString(value, charset)


new = Pyjo_UnicodeString.new
object = Pyjo_UnicodeString  # @ReservedAssignment
