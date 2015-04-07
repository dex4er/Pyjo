# -*- coding: utf-8 -*-

"""
Pyjo.Cookie.Request - HTTP request cookie
=========================================
::

    Pyjo.Cookie.Request

    cookie = Pyjo.Cookie.Request.new()
    cookie.name('foo')
    cookie.value('bar')
    print(cookie)

:mod:`Pyjo.Cookie.Request` is a container for HTTP request cookies based on
:rfc:`6265`.

Classes
-------
"""

import Pyjo.Cookie


class Pyjo_Cookie_Request(Pyjo.Cookie.object):
    """
    :mod:`Pyjo.Cookie.Request` inherits all attributes and methods from
    :mod:`Pyjo.Cookie` and implements the following new ones.
    """


new = Pyjo_Cookie_Request.new
object = Pyjo_Cookie_Request  # @ReservedAssignment
