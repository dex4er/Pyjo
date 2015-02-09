# -*- coding: utf-8 -*-

"""
Pyjo.Message.Response - HTTP Response
===================================

::

    import Pyjo.Message.Response

    # Parse
    res = Pyjo.Message.Response.new()
    res.parse(b"HTTP/1.0 200 OK\x0d\x0a")
    res.parse(b"Content-Length: 12\x0d\x0a")
    res.parse(b"Content-Type: text/plain\x0d\x0a\x0d\x0a")
    res.parse(b'Hello World!');
    print(res.code)
    print(res.headers.content_type)
    print(res.body)

    # Build
    res = Pyjo.Message.Response.new()
    res.code = 200
    res.headers.content_type = 'text/plain'
    res.body = b'Hello World!'
    print(res)

:mod:`Pyjo.Message.Response` is a container for HTTP Responses based on
:rfc:`7230` and
:rfc:`7231`.

Classes
-------
"""

import Pyjo.Message

from Pyjo.Regexp import m, s


class Pyjo_Message_Response(Pyjo.Message.object):
    """
    :mod:`Pyjo.Message.Response` inherits all attributes and methods from
    :mod:`Pyjo.Message` and implements the following new ones.
    """

    code = None
    message = None

    def extract_start_line(self):
        # We have a full response line
        self._buffer, g = self._buffer == s(br'^(.*?)\x0d?\x0a', '')
        if not g:
            return
        g = g[1] == m(br'^\s*HTTP/(\d\.\d)\s+(\d\d\d)\s*(.+)?$')
        if not g:
            return

        self.code = int(g[2])

        content = self.content
        if self.is_empty:
            content.skip_body = 1

        if content.auto_decompress is None:
            content.auto_decompress = True
        if content.auto_relax is None:
            content.auto_relax = True

        if g[1] == '1.0':
            content.expect_close = True

        self.version = g[1]
        self.message = g[3]
        return bool(self.message)

    def fix_headers(self):
        if self._fixed:
            return self
        super(Pyjo_Message_Response, self).fix_headers()

        # TODO Date
        return self

    @property
    def is_empty(self):
        code = self.code
        if not code:
            return
        else:
            return self.is_status_class(100) or code == 204 or code == 304

    def is_status_class(self, status_class):
        code = self.code
        if not code:
            return
        else:
            return code >= status_class and code < (status_class + 100)


new = Pyjo_Message_Response.new
object = Pyjo_Message_Response  # @ReservedAssignment
