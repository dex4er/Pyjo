# -*- coding: utf-8 -*-

r"""
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

from Pyjo.Regexp import r


re_line = r(br'^(.*?)\x0d?\x0a')
re_http = r(br'^\s*HTTP/(\d\.\d)\s+(\d\d\d)\s*(.+)?$')


class Pyjo_Message_Response(Pyjo.Message.object):
    """
    :mod:`Pyjo.Message.Response` inherits all attributes and methods from
    :mod:`Pyjo.Message` and implements the following new ones.
    """

    code = None
    message = None

    def extract_start_line(self):
        # We have a full response line
        m = re_line.search(self._buffer)
        if m:
            self._buffer = re_line.sub(b'', self._buffer, 1)
            line = m.group(1)
        else:
            return
        m = re_http.search(line)
        if not m:
            return

        version, code, message = m.groups()

        self.code = int(code)

        content = self.content
        if self.is_empty:
            content.skip_body = 1

        if content.auto_decompress is None:
            content.auto_decompress = True
        if content.auto_relax is None:
            content.auto_relax = True

        if version == '1.0':
            content.expect_close = True

        self.version = version
        self.message = message
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
