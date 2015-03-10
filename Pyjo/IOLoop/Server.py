"""
Pyjo.IOLoop.Server - Non-blocking TCP server
============================================
::

    import Pyjo.IOLoop.Server

    # Create listen socket
    server = Pyjo.IOLoop.Server.new()

    @server.on
    def accept(server, handle):
        ...

    server.listen(port=3000)

    # Start and stop accepting connections
    server.start()
    server.stop()

    # Start reactor if necessary
    if not server.reactor.is_running:
        server.reactor.start()

:mod:`Pyjo.IOLoop.Server` accepts TCP connections for :mod:`Pyjo.IOLoop`.

Events
------

:mod:`Pyjo.IOLoop.Server` inherits all events from :mod:`Pyjo.EventEmitter` and can
emit the following new ones.

accept
~~~~~~

    @server.on
    def accept(server, handle):
        ...

Emitted for each accepted connection.

Classes
-------
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Base import lazy
from Pyjo.Util import getenv, warn

import socket
import weakref


DEBUG = getenv('PYJO_IOLOOP_DEBUG', False)


class Pyjo_IOLoop_Server(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.IOLoop.Server` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    multi_accept = 50
    """::

        multi = server.multi_accept
        server.multi_accept = 100

    Number of connections to accept at once, defaults to ``50``.
    """

    reactor = lazy(lambda self: Pyjo.IOLoop.singleton.reactor)
    """::

        reactor = server.reactor
        server.reactor = Pyjo.Reactor.Poll.new()

    Low-level event reactor, defaults to the :attr:`reactor` attribute value of the
    global :mod:`Pyjo.IOLoop` singleton.
    """

    _handle = None
    _handles = lazy(lambda self: {})

    def __del__(self):
        if DEBUG:
            warn("-- Method {0}.__del__".format(self))

        if dir(self.reactor):
            if dir(self._handle) and self._handle:
                self.stop()
            for handle in self._handles.values():
                self.reactor.remove(handle)

    def generate_port(self):
        """::

            port = server.generate_port()

        Find a free TCP port, primarily used for tests.
        """
        listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen.bind(('127.0.0.1', 0))
        listen.listen(5)
        return listen.getsockname()[1]

    @property
    def handle(self):
        """::

            handle = server.handle

        Get handle for server.
        """
        return self._handle

    def listen(self, **kwargs):
        """::

            server.listen(port=3000)

        Create a new listen socket.

        These options are currently available:

        ``address``
            ::

                address='127.0.0.1'

            Local address to listen on, defaults to ``0.0.0.0``.

        ``backlog``
            ::

                backlog=128

            Maximum backlog size, defaults to :attr:`socket.SOMAXCONN`.

        ``port``
            ::

                port=80

            Port to listen on, defaults to a random port.

        ``reuse``
            ::

                reuse=True

            Allow multiple servers to use the same port with the :attr:`socket.SO_REUSEPORT` socket
            option.

        ``tls``
            ::

                tls=True

            Enable TLS.

        ``tls_ca``
            ::

                tls_ca='/etc/ssl/certs/ca-certificates.crt'

            Path to TLS certificate authority file.

        ``tls_cert``
            ::

                tls_cert='/etc/ssl/certs/ssl-cert-snakeoil.pem'

            Path to the TLS cert file, defaults to a built-in test certificate.

        ``tls_ciphers``
            ::

                tls_ciphers='AES128-GCM-SHA256:RC4:HIGH:!MD5:!aNULL:!EDH'

            Cipher specification string.

        ``tls_key``
            ::

                tls_key='/etc/ssl/private/ssl-cert-snakeoil.key'

            Path to the TLS key file, defaults to a built-in test key.

        ``tls_verify``
            ::

                tls_verify=0x00

            TLS verification mode, defaults to ``0x03``.
        """
        address = kwargs.get('address', '127.0.0.1')
        port = kwargs.get('port', 0)
        backlog = kwargs.get('backlog', socket.SOMAXCONN)

        # TODO Allow file descriptor inheritance
        # TODO Reuse file descriptor

        # New socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((address, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(0)
        s.listen(backlog)
        self._handle = s

    @property
    def port(self):
        """::

            port = server.port

        Get port this server is listening on.
        """
        return self._handle.getsockname()[1]

    def start(self):
        """::

            server.start()

        Start accepting connections.
        """
        def ready_cb(self, unused):
            self._accept()

        self = weakref.proxy(self)
        self.reactor.io(lambda reactor, write: ready_cb(self, reactor), self._handle)

    def stop(self):
        """::

            server.stop()

        Stop accepting connections.
        """
        self.reactor.remove(self._handle)
        self._handle = None

    def _accept(self):
        # Greedy accept
        for _ in range(0, self.multi_accept):
            try:
                (handle, unused) = self._handle.accept()
            except:
                return  # TODO EAGAIN because non-blocking mode
            if not handle:
                return
            handle.setblocking(0)

            # Disable Nagle's algorithm
            handle.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            self.emit('accept', handle)
            # self.reactor.remove(self._handle)
            # TODO TLS


new = Pyjo_IOLoop_Server.new
object = Pyjo_IOLoop_Server  # @ReservedAssignment
