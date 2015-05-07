# -*- coding: utf-8 -*-

"""
Pyjo.Server.CGI - CGI server
============================
::

    import Pyjo.Server.CGI
    from Pyjo.Util import b

    cgi = Pyjo.Server.CGI.new()
    cgi.unsubscribe('request')

    @cgi.on
    def request(cgi, tx):
        # Request
        method = tx.req.method
        path = tx.req.url.path

        # Response
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b("{0} request for {1}!".format(method, path))

        # Resume transaction
        tx.resume()

cgi.run()

:mod:`Pyjo.Server.CGI` is a simple and portable implementation of
:rfc:`3875`.

Events
------

:mod:`Pyjo.Server.CGI` inherits all events from :mod:`Pyjo.Server`.

Classes
-------
"""

import Pyjo.Server.Base


class Pyjo_Server_CGI(Pyjo.Server.Base.object):
    """
    :mod:`Pyjo.Server.CGI` inherits all attributes and methods from
    :mod:`Pyjo.Server.Base` and implements the following new ones.
    """


new = Pyjo_Server_CGI.new
object = Pyjo_Server_CGI  # @ReservedAssignment
