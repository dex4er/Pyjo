# -*- coding: utf-8 -*-

"""
Pyjo.Server.Base - HTTP/WebSocket server base class
===================================================
::

    import Pyjo.Server.Base

    class MyServer(Pyjo.Server.Base.object):

        def run(self):
            # Get a transaction
            tx = self.build_tx()

            # Emit "request" event
            self.emit('request', tx)

:mod:`Pyjo.Server` is an abstract base class for HTTP/WebSocket servers and server
interfaces, like :mod:`Pyjo.Server.CGI`, :mod:`Pyjo.Server.Daemon`
and :mod:`Pyjo.Server.WSGI`.

Events
------

:mod:`Pyjo.Server` inherits all events from :mod:`Pyjo.EventEmitter` and can emit the
following new ones.

request
~~~~~~~
::

    @server.on
    def request(server, tx):
        ...

Emitted when a request is ready and needs to be handled. ::

    server.unsubscribe('request')

    @server.on
    def request(server, tx):
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b'Hello World!'
        tx.resume()

Classes
-------
"""

import Pyjo.EventEmitter


class Pyjo_Server_Base(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Server.Base` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """


new = Pyjo_Server_Base.new
object = Pyjo_Server_Base  # @ReservedAssignment
