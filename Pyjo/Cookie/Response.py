# -*- coding: utf-8 -*-

"""
Pyjo.Cookie.Response - HTTP response cookie
===========================================
::

    Pyjo.Cookie.Response

    cookie = Pyjo.Cookie.Response.new()
    cookie.name('foo')
    cookie.value('bar')
    print(cookie)

:mod:`Pyjo.Cookie.Response` is a container for HTTP response cookies based on
:rfc:`6265`.

Classes
-------
"""

import Pyjo.Cookie


class Pyjo_Cookie_Response(Pyjo.Cookie.object):
    """
    :mod:`Pyjo.Cookie.Response` inherits all attributes and methods from
    :mod:`Pyjo.Cookie` and implements the following new ones.
    """


new = Pyjo_Cookie_Response.new
object = Pyjo_Cookie_Response  # @ReservedAssignment
