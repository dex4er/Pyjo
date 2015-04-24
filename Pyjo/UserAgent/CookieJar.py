# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent.CookieJar - Cookie jar for HTTP user agents
==========================================================
::

    import Pyjo.UserAgent.CookieJar

    # Add response cookies
    jar = Pyjo.UserAgent.CookieJar.new()
    jar.add(
        Pyjo.UserAgent.CookieJar.new([
            'name': 'foo',
            'value': 'bar',
            'domain': 'localhost',
            'path': '/test'
        ])
    )

    # Find request cookies
    for cookie in jar.find(Pyjo.URL.new('http://localhost/test')):
        print(cookie.name)
        print(cookie.value)

:mod:`Pyjo.UserAgent.CookieJar` is the transaction building and manipulation
framework used by :mod:`Pyjo.UserAgent`.

Classes
-------
"""

import Pyjo.Base

from Pyjo.Base import lazy


class Pyjo_UserAgent_CookieJar(Pyjo.Base.object):
    """
    :mod:`Pyjo.UserAgent.CookieJar` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """


new = Pyjo_UserAgent_CookieJar.new
object = Pyjo_UserAgent_CookieJar  # @ReservedAssignment
