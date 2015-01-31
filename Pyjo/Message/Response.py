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

from Pyjo.Base import lazy


class Pyjo_Message_Response(Pyjo.Message.object):
    """
    :mod:`Pyjo.Message.Response` inherits all attributes and methods from
    :mod:`Pyjo.Message` and implements the following new ones.
    """


new = Pyjo_Message_Response.new
object = Pyjo_Message_Response  # @ReservedAssignment
