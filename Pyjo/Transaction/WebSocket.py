# -*- coding: utf-8 -*-

"""
Pyjo.Transaction.WebSocket - WebSocket transaction
==================================================
::

    import Pyjo.Transaction.WebSocket

    # Send and receive WebSocket messages
    ws = Pyjo.Transaction.WebSocket.new()
    ws.send('Hello World!')

    @ws.on
    def message(ws, msg):
        print("Message: {0}".format(repr(msg)))

    @ws.on
    def finish(ws, code, reason):
        print("WebSocket closed with status {0}".format(code))

:mod:`Pyjo.Transaction.WebSocket` is a container for WebSocket transactions based
on :rfc:`6455`.

Events
------

:mod:`Pyjo.Transaction.WebSocket` inherits all events from :mod:`Pyjo.Transaction` and
can emit the following new ones.

binary
~~~~~~
::

    @ws.on
    def binary(ws, chunk):
        ...

Emitted when a complete WebSocket binary message has been received.

drain
~~~~~
::

    @ws.on
    def drain(ws):
        ...

Emitted once all data has been sent.

finish
~~~~~~
::

    @ws.on
    def finish(ws, code, reason):
        ...

Emitted when the WebSocket connection has been closed.

frame
~~~~~
::

    @ws.on
    def frame(ws, frame):
        ...

Emitted when a WebSocket frame has been received. ::

    ws.unsubscribe('frame')

    @ws.on
    def frame(ws, frame):
        print("FIN: {0}.format(frame))
        print("RSV1: {1}.format(frame))
        print("RSV2: {2}.format(frame))
        print("RSV3: {3}.format(frame))
        print("Opcode: {4}.format(frame))
        print("Payload: {5}.format(frame))

json
~~~~
::

    @ws.on
    def json(ws, json):
        ...

Emitted when a complete WebSocket message has been received, all text and
binary messages will be automatically JSON decoded. Note that this event only
gets emitted when it has at least one subscriber. ::

    @ws.on
    def json(ws, json):
        print("Message: {msg}".format(json))

message
~~~~~~~
::

    @ws.on
    def message(ws, msg):
        ...

Emitted when a complete WebSocket message has been received, text messages will
be automatically decoded. Note that this event only gets emitted when it has at
least one subscriber.

text
~~~~
::

    @ws.on
    def text(ws, chunk):
        ...

Emitted when a complete WebSocket text message has been received.

Classes
-------
"""

import Pyjo.Transaction

from Pyjo.Util import notnone


class Pyjo_Transaction_WebSocket(Pyjo.Transaction.object):
    """
    :mod:`Pyjo.Transaction.WebSocket` inherits all attributes and methods from
    :mod:`Pyjo.Transaction` and implements the following new ones.
    """


new = Pyjo_Transaction_WebSocket.new
object = Pyjo_Transaction_WebSocket  # @ReservedAssignment
