# -*- coding: utf-8 -*-

"""
Pyjo.Headers - Headers
======================
::

    import Pyjo.Headers

    # Parse
    headers = Pyjo.Headers.new
    headers.parse(b"Content-Length: 42\x0d\x0a")
    headers.parse(b"Content-Type: text/html\x0d\x0a\x0d\x0a")
    print(headers.content_length)
    print(headers.content_type)

    # Build
    headers = Pyjo.Headers.new
    headers.content_length = 42
    headers.content_type = 'text/plain'
    print(headers.to_str())

:mod:`Pyjo.Headers` is a container for HTTP headers based on
:rfc:`7230` and
:rfc:`7231`.
"""

import Pyjo.Base
import Pyjo.Mixin.String

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv


NORMALCASE = {}


class Pyjo_Headers(Pyjo.Base.object, Pyjo.Mixin.String.object):
    """::

        headers = Pyjo.headers.new()
        headers = Pyjo.headers.new(b"Content-Type: text/plain\x0d\x0a")

    Construct a new :mod`Pyjo.Headers` object and :meth:`parse` headers if necessary.
    """

    max_line_size = int(getenv('PYJO_MAX_LINE_SIZE', 0)) or 10240
    max_lines = int(getenv('PYJO_MAX_LINES', 0)) or 100

    _buffer = b''
    _cache = lazy(lambda self: [])
    _headers = lazy(lambda self: {})
    _normalcase = lazy(lambda self: {})
    _state = None

    def __init__(self, path=None):
        super(Pyjo_Headers, self).__init__()
        if path is not None:
            self.parse(path)

    def add(self, name, *args):
        """::

            headers = headers.add('Foo', 'one value')
            headers = headers.add('Foo', 'first value', 'second value')

        Add one or more header values with one or more lines. ::

            # "Vary: Accept"
            # "Vary: Accept-Encoding"
            headers.set(vary='Accept').add('Vary', 'Accept-Encoding').to_str()
        """
        # Make sure we have a normal case entry for name
        key = b(name.lower(), 'ascii')
        if key not in NORMALCASE:
            self._normalcase[key] = name
        if key not in self._headers:
            self._headers[key] = []
        for value in args:
            self._headers[key].append(b(value, 'ascii'))

        return self

    def parse(self, string):
        """::

            headers = headers.parse(b"Content-Type: text/plain\x0d\x0a\x0d\x0a")

        Parse formatted headers.
        """
        self._state = 'headers'
        self._buffer += b(string, 'ascii')
        if self._cache:
            headers = self._cache
        else:
            headers = []
        size = self.max_line_size
        lines = self.max_lines
        pos = 0

        for g in m(br'(.*?)\x0d?\x0a', 'g').match(self._buffer):
            pos += len(g[0])
            line = g[1]

            # Check line size limit
            if len(g[0]) > size or len(headers) >= lines:
                self._buffer = self._buffer[pos:]
                self._state = 'finished'
                self._limit = True
                return self

            # New header
            g = line == m(br'^(\S[^:]*)\s*:\s*(.*)$')
            if g:
                headers.append((g[1], g[2]))

            else:
                # Multiline
                line, g = line == s(br'^\s+', b'')
                if g and headers:
                    headers[-1][1] += b' ' + line

                # Empty line
                else:
                    for h in headers:
                        self.add(h[0], h[1])
                    self._buffer = self._buffer[pos:]
                    self.state = 'finished'
                    self.cache = []
                    return self

        self._buffer = self._buffer[pos:]

        # Check line size limit
        if len(self._buffer) > size:
            self._state = 'finished'
            self._limit = True

        return self

    def to_str(self):
        """::

            string = headers.to_str()

        Turn headers into a string, suitable for HTTP messages.
        """
        headers = []
        return b"\x0d\x0a".join(headers)


new = Pyjo_Headers.new
object = Pyjo_Headers  # @ReservedAssignment
