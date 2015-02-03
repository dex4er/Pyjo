# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent.Transactor - User agent transactor
=================================================

::

    import Pyjo.UserAgent.Transactor

    # Simple GET request
    t = Pyjo.UserAgent.Transactor.new()
    print(t.tx('GET', 'http://example.com').req)

    # PATCH request with "Do Not Track" header and content
    print(t.tx('PATCH', 'example.com', headers={'DNT': 1}, data='Hi!').req)

    # POST request with form-data
    print(t.tx('POST', 'example.com', form={'a': 'b'}).req)

    # PUT request with JSON data
    print(t.tx('PUT', 'example.com', json={'a': 'b'}).req)

:mod:`Pyjo.UserAgent.Transactor` is the transaction building and manipulation
framework used by :mod:`Pyjo.UserAgent`.

Classes
-------
"""

import Pyjo.Base

from Pyjo.Base import lazy


class Pyjo_UserAgent_Transactor(Pyjo.Base.object):
    """
    :mod:`Pyjo.UserAgent.Transactor` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """

    def tx(self, url, **kwargs):
        ...


new = Pyjo_UserAgent_Transactor.new
object = Pyjo_UserAgent_Transactor  # @ReservedAssignment
