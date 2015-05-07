# -*- coding: utf-8 -*-

"""
Pyjo.Server.WSGI - WSGI server
==============================
::

    import Pyjo.Server.WSGI
    from Pyjo.Util import b

    wsgi = Pyjo.Server.WSGI.new()
    wsgi.unsubscribe('request')

    @wsgi.on
    def request(wsgi, tx):
        # Request
        method = tx.req.method
        path = tx.req.url.path

        # Response
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b("{0} request for {1}!".format(method, path))

        # Resume transaction
        tx.resume()

wsgi.to_wsgi_app()

:mod:`Pyjo.Server.WSGI` allows :mod:`Pyjoyment` applications to run on all ``WSGI``
compatible servers.

Events
------

:mod:`Pyjo.Server.WSGI` inherits all events from :mod:`Pyjo.Server`.

Classes
-------
"""

import Pyjo.Server.Base


class Pyjo_Server_WSGI(Pyjo.Server.Base.object):
    """
    :mod:`Pyjo.Server.WSGI` inherits all attributes and methods from
    :mod:`Pyjo.Server.Base` and implements the following new ones.
    """


new = Pyjo_Server_WSGI.new
object = Pyjo_Server_WSGI  # @ReservedAssignment
