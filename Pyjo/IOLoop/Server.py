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
::

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
from Pyjo.Regexp import m, s
from Pyjo.Util import getenv, setenv, warn

import os
import re
import socket
import weakref


DEBUG = getenv('PYJO_IOLOOP_DEBUG', False)
DIE = getenv('PYJO_IOLOOP_DIE', False)

CERT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'server.crt')
KEY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'server.key')


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


class Pyjo_IOLoop_Server(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.IOLoop.Server` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    handle = None
    """::

        handle = stream.handle

    Handle for stream.
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

    _handles = lazy(lambda self: {})
    _reuse = None
    _tls_kwargs = lazy(lambda self: {})

    def __del__(self):
        if DEBUG:
            warn("-- Method {0}.__del__".format(self))

        if self._reuse:
            reuse = getenv('PYJO_REUSE')
            reuse -= s(r'(?:^|\,){0}'.format(re.escape(reuse)), '')
            setenv('PYJO_REUSE', reuse)

        if dir(self.reactor):
            if dir(self.handle) and self.handle:
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

        address_port = '{0}:{1}'.format(address, port)
        g = getenv('PYJO_REUSE', '') == m(r'(?:^|\,){0}:(\d+)'.format(re.escape(address_port)))
        if g:
            fd = int(g[1])
        else:
            fd = None

        # Reuse file descriptor
        if fd:
            s = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)

        # New socket
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if kwargs.get('reuse'):
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind((address, port))

            fd = s.fileno()
            self._reuse = '{0}:{1}:{2}'.format(address, s.getsockname()[1], fd)
            if len(getenv('PYJO_REUSE', '')):
                setenv('PYJO_REUSE', getenv('PYJO_REUSE') + ',' + self._reuse)
            else:
                setenv('PYJO_REUSE', self._reuse)

        s.setblocking(0)
        s.listen(backlog)
        self.handle = s

        if not kwargs.get('tls'):
            return

        tls_kwargs = {
            'do_handshake_on_connect': False,
            'server_side': True,
            'ca_certs': kwargs.get('tls_ca'),
            'certfile': kwargs.get('tls_cert', CERT),
            'keyfile': kwargs.get('tls_key', KEY),
            'ciphers': kwargs.get('tls_ciphers'),
        }

        if 'tls_verify' in kwargs:
            tls_kwargs['cert_reqs'] = kwargs['tls_verify']
        else:
            if tls_kwargs['ca_certs']:
                tls_kwargs['cert_reqs'] = 0x03
            else:
                tls_kwargs['cert_reqs'] = 0x00

        self._tls_kwargs = tls_kwargs

    @property
    def port(self):
        """::

            port = server.port

        Get port this server is listening on.
        """
        return self.handle.getsockname()[1]

    def start(self):
        """::

            server.start()

        Start accepting connections.
        """
        def ready_cb(self, unused):
            self._accept()

        self = weakref.proxy(self)
        self.reactor.io(lambda reactor, write: ready_cb(self, reactor), self.handle)

    def stop(self):
        """::

            server.stop()

        Stop accepting connections.
        """
        self.reactor.remove(self.handle)

    def _accept(self):
        # Greedy accept
        for _ in range(0, self.multi_accept):
            try:
                (handle, unused) = self.handle.accept()
            except:
                return  # TODO EAGAIN because non-blocking mode
            if not handle:
                return
            handle.setblocking(0)

            # Disable Nagle's algorithm
            handle.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            self.emit('accept', handle)

            if self._tls_kwargs:
                try:
                    ssl_handle = ssl.wrap_socket(handle, **self._tls_kwargs)
                    self._handles[ssl_handle] = ssl_handle
                    self._handshake(ssl_handle)
                except SSLError as ex:
                    if DIE:
                        raise ex
                    else:
                        return self.emit('error', 'TLS upgrade failed')

    def _handshake(self, handle):
        self = weakref.proxy(self)
        self.reactor.io(lambda reactor, write: self._tls(handle), handle)

    def _tls(self, handle):
        handle = self._handles[handle]
        # Accepted
        try:
            handle.do_handshake()
            # Accepted
            self.reactor.remove(handle)
            del self._handles[handle]
            return self.emit('accept', handle)
        except SSLWantReadError:
            return self.reactor.watch(handle, True, False)
        except SSLWantWriteError:
            return self.reactor.watch(handle, True, True)
        except SSLError as ex:
            self.reactor.remove(handle)  # TODO remove here?
            raise ex

        return self.reactor.watch(handle, True, True)


new = Pyjo_IOLoop_Server.new
object = Pyjo_IOLoop_Server  # @ReservedAssignment
