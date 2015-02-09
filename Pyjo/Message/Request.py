# -*- coding: utf-8 -*-

"""
Pyjo.Message.Request - HTTP request
===================================

::

    import Pyjo.Message.Request

    # Parse
    req = Pyjo.Message.Request.new()
    req.parse(b"GET /foo HTTP/1.0\x0d\x0a")
    req.parse(b"Content-Length: 12\x0d\x0a")
    req.parse(b"Content-Type: text/plain\x0d\x0a\x0d\x0a")
    req.parse(b'Hello World!');
    print(req.method)
    print(req.headers.content_type)
    print(req.body)

    # Build
    req = Pyjo.Message.Request.new()
    req.url.parse('http://127.0.0.1/foo/bar');
    req.method = 'GET'
    print(req)

:mod:`Pyjo.Message.Request` is a container for HTTP requests based on
:rfc:`7230`,
:rfc:`7231`,
:rfc:`7235` and
:rfc:`2817`.

Classes
-------
"""

import Pyjo.Message
import Pyjo.URL

from Pyjo.Base import lazy
from Pyjo.Util import b


class Pyjo_Message_Request(Pyjo.Message.object):
    """
    :mod:`Pyjo.Message.Request` inherits all attributes and methods from
    :mod:`Pyjo.Message` and implements the following new ones.
    """

    method = 'GET'
    url = lazy(lambda self: Pyjo.URL.new())

    _start_buffer = None

    def fix_headers(self):
        if self._fixed:
            return self

        super(Pyjo_Message_Request, self).fix_headers()

        # Host
        url = self.url
        headers = self.headers
        if not headers.host:
            headers.host = url.host_port

        # TODO
        return self

    def get_start_line_chunk(self, offset):
        if self._start_buffer is None:

            # Path
            url = self.url
            path = url.path_query
            if not path.startswith('/'):
                path = '/' + path

            # TODO CONNECT
            method = self.method.upper()

            # TODO Proxy

            self._start_buffer = b(method) + b' ' + b(path) + b' HTTP/' + b(self.version) + b'\x0d\x0a'

        self.emit('progress', 'start_line', offset)
        return self._start_buffer[offset:offset + 131072]


new = Pyjo_Message_Request.new
object = Pyjo_Message_Request  # @ReservedAssignment
