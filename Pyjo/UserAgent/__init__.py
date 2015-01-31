# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent - Non-blocking I/O HTTP and WebSocket user agent
===============================================================

::

    import Pyjo.UserAgent

    # Say hello to the Unicode snowman with "Do Not Track" header
    ua = Pyjo.UserAgent.new()
    print(ua.get(u'www.☃.net?hello=there', headers={'DNT': 1}).res.body

    # Form POST with exception handling
    tx = ua.post('https://metacpan.org/search', form={'q': 'pyjo'})
    if tx.success:
        print(tx.res.body)
    else:
        err = tx.error
        if err.code:
            raise Exception('{0} response: {1}'.format(err.code, err.message))
        else:
            raise Exception('Connection error: {0}'.format(err.message))

:mod:`Pyjo.UserAgent` is a full featured non-blocking I/O HTTP.

Classes
-------
"""

import Pyjo.EventEmitter

from Pyjo.Base import lazy


class Pyjo_UserAgent(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.UserAgent` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """


new = Pyjo_UserAgent.new
object = Pyjo_UserAgent  # @ReservedAssignment
