# -*- coding: utf-8 -*-

"""
Pyjo.TextStream - TextStream
============================
::

    import Pyjo.TextStream

    stream = Pyjo.TextStream.new('foo_bar_baz')
"""


from __future__ import print_function

import sys

import Pyjo.ByteStream
import Pyjo.Util


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
    def __new__(cls, value=u'', charset=DEFAULT_CHARSET):
        return super(Pyjo_TextStream, cls).__new__(cls, Pyjo.Util.u(value, charset))

    def __repr__(self):
        return "{0}.new({1})".format(self.__module__, super(Pyjo_TextStream, self).__repr__())

    def html_unescape(self):
        """::

            stream = stream.html_unescape()

        Unescape all HTML entities in bytestream with :func:`Pyjo.Util.html_unescape`. ::

            b('&lt;html&gt;').html_unescape().url_escape().say()
        """
        return self.new(Pyjo.Util.html_unescape(self))

    def encode(self, charset=DEFAULT_CHARSET):
        """::

            stream = stream.encode
            stream = stream.encode('iso-8859-1')

        Encode bytestream, defaults to ``utf-8``, and return new :mod:`Pyjo.ByteStream` object. ::

            stream.trim().quote().encode().say()
        """
        return Pyjo.ByteStream.new(super(Pyjo_TextStream, self).encode(charset))

    @classmethod
    def new(cls, value=u'', charset=DEFAULT_CHARSET):
        return Pyjo_TextStream(value, charset)

    def say(self, **kwargs):
        """::

            stream = stream.say()
            stream = stream.say(file=sys.stderr, end='', flush=True)

        Print bytestream to handle and append a newline, defaults to :attr:`sys.stdout`.
        """
        if 'flush' in kwargs and sys.version_info < (3, 0):
            flush = kwargs.pop('flush')
        else:
            flush = False
        print(self, **kwargs)
        if flush:
            f = kwargs.get('file', sys.stdout)
            f.flush()
        return self

    def xml_escape(self):
        """::

            stream = stream.xml_escape()

        Escape only the characters ``&``, ``<``, ``>``, ``"`` and ``'`` in bytestream with :func:`Pyjo.Util.xml_escape`.
        """
        return self.new(Pyjo.Util.xml_escape(self))


def u(value=u'', charset=DEFAULT_CHARSET):
    """::

        stream = u('test123')

    Construct a new :mod:`Pyjo.TextStream` object.
    """
    return Pyjo_TextStream(value, charset)


new = Pyjo_TextStream.new
object = Pyjo_TextStream  # @ReservedAssignment
