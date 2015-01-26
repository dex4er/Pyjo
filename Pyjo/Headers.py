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


class Pyjo_Headers(Pyjo.Base.object, Pyjo.Mixin.String.object):
    """::

        headers = Pyjo.headers.new()
        headers = Pyjo.headers.new(b"Content-Type: text/plain\x0d\x0a")

    Construct a new :mod`Pyjo.Headers` object and :meth:`parse` headers if necessary.
    """

    def __init__(self, path=None):
        super(Pyjo_Headers, self).__init__()
        if path is not None:
            self.parse(path)

    def to_str(self):
        """::

            string = headers.to_str()

        Turn headers into a string, suitable for HTTP messages.
        """
        headers = []
        return b"\x0d\x0a".join(headers)


new = Pyjo_Headers.new
object = Pyjo_Headers  # @ReservedAssignment
