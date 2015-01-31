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

from Pyjo.Base import lazy


class Pyjo_Message_Request(Pyjo.Message.object):
    """
    :mod:`Pyjo.Message.Request` inherits all attributes and methods from
    :mod:`Pyjo.Message` and implements the following new ones.
    """


new = Pyjo_Message_Request.new
object = Pyjo_Message_Request  # @ReservedAssignment
