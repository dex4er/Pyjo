"""
Pyjo.IOLoop.Client - Non-blocking TCP/UDP client
================================================
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

    client.connect(address='example.com', port=80, proto='tcp')

    # Start reactor if necessary
    if not client.reactor.is_running:
        client.reactor.start()

:mod:`Pyjo.IOLoop.Client` opens TCP/UDP connections for :mod:`Pyjo.IOLoop`.

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


DEBUG = getenv('PYJO_IOLOOP_DEBUG', False)
DIE = getenv('PYJO_IOLOOP_DIE', False)


NoneType = None.__class__

if getenv('PYJO_NO_TLS', False):
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


SOCK = {
    'tcp': socket.SOCK_STREAM,
    'udp': socket.SOCK_DGRAM,
}


class Pyjo_IOLoop_Client(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.IOLoop.Client` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    handle = None
    """::

        handle = stream.handle

    Handle for stream.
    """

    reactor = lazy(lambda self: Pyjo.IOLoop.singleton.reactor)
    """::

        reactor = client.reactor
        client.reactor = Pyjo.Reactor.Poll.new()

    Low-level event reactor, defaults to the :attr:`reactor` attribute value of the
    global :mod:`Pyjo.IOLoop` singleton.
    """

    _timer = None

    def __del__(self):
        if DEBUG:
            warn("-- Method {0}.__del__".format(self))

        try:
            self.close()
        except:
            pass

    def close(self):
        """::

            client.close()

        Close all server connections and server itself.
        """
        if self.handle:
            self.handle.close()

        self._cleanup()

    def connect(self, **kwargs):
        """::

            client.connect(address='127.0.0.1', port=3000)

        Open a socket connection to a remote host.

        These options are currently available:

        ``address``
            ::

                address='mojolicio.us'

            Address or host name of the peer to connect to, defaults to ``127.0.0.1``.

        ``handle``
            ::

                handle=handle

            Use an already prepared handle.

        ``local_address``
            ::

                local_address='127.0.0.1'

            Local address to bind to.

        ``port``
            ::

                port=80

            Port to connect to, defaults to ``80`` or ``443`` with ``tls`` option.

        ``proto``
            ::

                proto='tcp'

            Transport protocol: ``tcp`` or ``udp``, defaults to ``tcp``.

        ``timeout``
            ::

                timeout=15

            Maximum amount of time in seconds establishing connection may take before
            getting canceled, defaults to ``10``.

        ``tls``
            ::

                tls=True

            Enable TLS.

        ``tls_ca``
            ::

                tls_ca='/etc/ssl/certs/ca-certificates.crt'

            Path to TLS certificate authority file. Also activates hostname verification.

        ``tls_cert``
            ::

                tls_cert='/etc/ssl/certs/ssl-cert-snakeoil.pem'

            Path to the TLS certificate file.

        ``tls_key``
            ::

                tls_key='/etc/ssl/private/ssl-cert-snakeoil.key'

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

        if self.handle:
            reactor.remove(self.handle)
            self.handle = None

        return self

    def _connect(self, **kwargs):
        handle = kwargs.get('handle')
        if not handle:
            handle = self.handle
        if not handle:
            address = kwargs.get('address', 'localhost')
            port = self._port(**kwargs)
            proto = kwargs.get('proto', 'tcp')

            handle = socket.socket(socket.AF_INET, SOCK[proto])
            handle.connect((address, port))
            # TODO return self.emit('error', "Can't connect: " + str(e))
            self.handle = handle

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
        handle = self.handle

        if handle.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) == socket.SOCK_DGRAM:
            return self._cleanup().emit('connect', handle)

        # Disable Nagle's algorithm
        handle.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # TODO TLS, Socks
        return self._try_tls(**kwargs)

    def _tls(self):
        handle = self.handle

        try:
            handle.do_handshake()
            # Connected
            return self._cleanup().emit('connect', handle)
        except SSLWantReadError:
            return self.reactor.watch(handle, True, False)
        except SSLWantWriteError:
            return self.reactor.watch(handle, True, True)
        except SSLError as ex:
            if ex.strerror == 'The operation did not complete (read)':
                return self.reactor.watch(handle, True, False)
            elif ex.strerror == 'The operation did not complete (write)':
                return self.reactor.watch(handle, True, True)
            self.reactor.remove(handle)
            raise ex

        return self.reactor.watch(handle, True, True)

    def _try_tls(self, **kwargs):
        handle = self.handle
        if not kwargs.get('tls', False) or (TLS and isinstance(handle, ssl.SSLSocket)):
            return self._cleanup().emit('connect', handle)
        if not TLS:
            return self.emit('error', 'ssl required for TLS support')

        tls_kwargs = {
            'do_handshake_on_connect': False,
            'server_side': False,
            'ca_certs': kwargs.get('tls_ca'),
            'certfile': kwargs.get('tls_cert'),
            'keyfile': kwargs.get('tls_key'),
        }

        if tls_kwargs['ca_certs']:
            tls_kwargs['cert_reqs'] = ssl.CERT_REQUIRED

        reactor = self.reactor
        reactor.remove(handle)

        try:
            ssl_handle = ssl.wrap_socket(handle, **tls_kwargs)
            self.handle = ssl_handle
        except SSLError as ex:
            if DIE:
                raise ex
            else:
                return self.emit('error', 'TLS upgrade failed')

        reactor.io(lambda reactor, write: self._tls(), ssl_handle).watch(ssl_handle, False, True)


new = Pyjo_IOLoop_Client.new
object = Pyjo_IOLoop_Client  # @ReservedAssignment
