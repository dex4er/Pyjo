# -*- coding: utf-8 -*-

"""
Pyjo.Transaction.HTTP - HTTP transaction
========================================

::

    import Pyjo.Transaction.HTTP

    # Client
    tx = Pyjo.Transaction.HTTP.new()
    tx.req.method = 'GET'
    tx.req.url.parse('http://example.com')
    tx.req.headers.accept = 'application/json'
    print(tx.res.code)
    print(tx.res.headers.content_type)
    print(tx.res.body)
    print(tx.remote_address)

:mod:`Pyjo.Transaction.HTTP` is a container for HTTP transactions based on
:rfc:`7230` and
:rfc:`7231`.

Classes
-------
"""

import Pyjo.Transaction

from Pyjo.Base import lazy


class Pyjo_Transaction_HTTP(Pyjo.Transaction.object):
    """
    :mod:`Pyjo.Transaction.HTTP` inherits all attributes and methods from
    :mod:`Pyjo.Transaction` and implements the following new ones.
    """


new = Pyjo_Transaction_HTTP.new
object = Pyjo_Transaction_HTTP  # @ReservedAssignment
