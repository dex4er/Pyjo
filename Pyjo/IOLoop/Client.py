"""
Pyjo.IOLoop.Client - Non-blocking TCP client
============================================
::

    import Pyjo.IOLoop.Client

    # Create socket connection
    client = Pyjo.IOLoop.Client.new()

    @client.on
    def connect(client, handle):
        ...

    @client.on
    def error(client, err):
        ...

    client.connect(address='example.com', port=80)

    # Start reactor if necessary
    if not client.reactor.is_running:
        client.reactor.start()

:mod:`Pyjo.IOLoop.Client` opens TCP connections for :mod:`Pyjo.IOLoop`.

Events
------

:mod:`Pyjo.IOLoop.Client` inherits all events from :mod:`Pyjo.EventEmitter` and can
emit the following new ones.

connect
~~~~~~~
::

    @client.on
    def connect(client, handle):
        ...

Emitted once the connection is established.

error
~~~~~
::

    @client.on
    def error(client, err):
        ...

Emitted if an error occurs on the connection, fatal if unhandled.

Classes
-------
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Base import lazy
from Pyjo.Util import getenv, warn

import socket
import weakref


NoneType = None.__class__

if getenv('PYJO_NO_TLS', 0):
    TLS = False
    TLS_WANT_ERROR = None
else:
    try:
        import ssl
        from ssl import SSLError
        TLS = True
        try:
            from ssl import SSLWantReadError, SSLWantWriteError
            TLS_WANT_ERROR = True
        except ImportError:
            TLS_WANT_ERROR = False
    except ImportError:
        TLS = None
        TLS_WANT_ERROR = None

if not TLS:
    SSLError = NoneType
if not TLS_WANT_ERROR:
    SSLWantReadError = SSLWantWriteError = NoneType


DEBUG = getenv('PYJO_IOLOOP_DEBUG', False)


class Pyjo_IOLoop_Client(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.IOLoop.Client` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    reactor = lazy(lambda self: Pyjo.IOLoop.singleton.reactor)
    """::

        reactor = client.reactor
        client.reactor = Pyjo.Reactor.Poll.new()

    Low-level event reactor, defaults to the :attr:`reactor` attribute value of the
    global :mod:`Pyjo.IOLoop` singleton.
    """

    _handle = None
    _timer = None

    def __del__(self):
        if DEBUG:
            warn("-- Method {0}.__del__".format(self))

        self._cleanup()

    def connect(self, **kwargs):
        """::

            client.connect(address='127.0.0.1', port=3000)

        Open a socket connection to a remote host.

        These options are currently available: ::

            address='mojolicio.us'

        Address or host name of the peer to connect to, defaults to ``127.0.0.1``. ::

            handle=handle

        Use an already prepared handle. ::

            local_address='127.0.0.1'

        Local address to bind to. ::

            port=80

        Port to connect to, defaults to ``80`` or ``443`` with ``tls`` option. ::

            timeout=15

        Maximum amount of time in seconds establishing connection may take before
        getting canceled, defaults to ``10``. ::

            tls=True

        Enable TLS. ::

            tls_ca='/etc/tls/ca.crt'

        Path to TLS certificate authority file. Also activates hostname verification. ::

            tls_cert='/etc/tls/client.crt'

        Path to the TLS certificate file. ::

            tls_key='/etc/tls/client.key'

        Path to the TLS key file.
        """

        reactor = self.reactor
        timeout = kwargs.get('timeout', 10)

        # Timeout
        self = weakref.proxy(self)

        def timeout_cb(self):
            if dir(self):
                self.emit('error', 'Connect timeout')

        self._timer = reactor.timer(lambda reactor: timeout_cb(self), timeout)

        # Blocking name resolution
        def resolved_cb(self):
            if dir(self):
                self._connect(**kwargs)

        return reactor.next_tick(lambda reactor: resolved_cb(self))

    def _cleanup(self):
        reactor = self.reactor

        if not dir(reactor):
            return

        if self._timer:
            reactor.remove(self._timer)
            self._timer = None

        if self._handle:
            reactor.remove(self._handle)
            self._handle = None

        return self

    def _connect(self, **kwargs):
        handle = kwargs.get('handle')
        if not handle:
            handle = self._handle
        if not handle:
            address = kwargs.get('address', 'localhost')
            port = self._port(**kwargs)

            handle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            handle.connect((address, port))
            # TODO return self.emit('error', "Can't connect: " + str(e))
            self._handle = handle

        handle.setblocking(0)

        # Wait for handle to become writable
        self = weakref.proxy(self)

        def ready_cb(self, loop, **kwargs):
            if dir(self):
                self._ready(**kwargs)

        self.reactor.io(lambda reactor, write: ready_cb(self, reactor, **kwargs), handle).watch(handle, False, True)

    def _port(self, **kwargs):
        port = kwargs.get('port')
        if not port:
            port = 80
        return port

    def _ready(self, **kwargs):
        # Retry or handle exceptions
        handle = self._handle

        # Disable Nagle's algorithm
        handle.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # TODO TLS, Socks
        return self._try_tls(**kwargs)

    def _tls(self):
        handle = self._handle
        while True:
            try:
                handle.do_handshake()
                # Connected
                return self._cleanup().emit('connect', handle)
            except SSLWantReadError:
                return self.reactor.watch(handle, True, False)
            except SSLWantWriteError:
                return self.reactor.watch(handle, True, True)
            except SSLError:
                return self.reactor.watch(handle, True, True)
        return self.emit('error', 'TLS upgrade failed')

    def _try_tls(self, **kwargs):
        handle = self._handle
        if not kwargs.get('tls', False) or (TLS and isinstance(handle, ssl.SSLSocket)):
            return self._cleanup().emit('connect', handle)
        if not TLS:
            return self.emit('error', 'ssl required for TLS support')

        reactor = self.reactor
        reactor.remove(handle)
        try:
            ssl_handle = ssl.wrap_socket(handle, do_handshake_on_connect=False) # TODO options
            self._handle = ssl_handle
        except SSLError:
            return self.emit('error', 'TLS upgrade failed')
        reactor.io(lambda reactor, write: self._tls(), ssl_handle).watch(ssl_handle, False, True)


new = Pyjo_IOLoop_Client.new
object = Pyjo_IOLoop_Client  # @ReservedAssignment
