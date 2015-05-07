# -*- coding: utf-8 -*-

"""
Pyjo.Server.Daemon - Non-blocking I/O HTTP and WebSocket server
===============================================================
::

    import Pyjo.Server.Daemon
    from Pyjo.Util import b

    daemon = Pyjo.Server.Daemon.new(listen=['http://*:8080'])
    daemon.unsubscribe('request')

    @daemon.on
    def request(daemon, tx):
        # Request
        method = tx.req.method
        path = tx.req.url.path

        # Response
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b("{0} request for {1}!".format(method, path))

        # Resume transaction
        tx.resume()

daemon.run()

:mod:`Pyjo.Server.Daemon` is a full featured, highly portable non-blocking I/O
HTTP and WebSocket server, with IPv6, TLS, Comet (long polling), keep-alive and
multiple event loop support.

Signals
-------

The :mod:`Pyjo.Server.Daemon` process can be controlled at runtime with the
following signals.

INT, TERM
~~~~~~~~~

Shut down server immediately.

Events
------

:mod:`Pyjo.Server.Daemon` inherits all events from :mod:`Pyjo.Server`.

Classes
-------
"""

import Pyjo.Server.Base


class Pyjo_Server_Daemon(Pyjo.Server.Base.object):
    """
    :mod:`Pyjo.Server.Daemon` inherits all attributes and methods from
    :mod:`Pyjo.Server.Base` and implements the following new ones.
    """


new = Pyjo_Server_Daemon.new
object = Pyjo_Server_Daemon  # @ReservedAssignment
