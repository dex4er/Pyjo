"""
Pyjo.IOLoop.Client
"""

import socket
import weakref

from socket import AF_INET, IPPROTO_TCP, TCP_NODELAY, SOCK_STREAM

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Util import getenv, warn


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


DEBUG = getenv('PYJO_IOLOOP_CLIENT_DEBUG', 0)


class Pyjo_IOLoop_Client(Pyjo.EventEmitter.object):

    reactor = None
    handle = None

    _timer = None

    def __init__(self, **kwargs):
        if DEBUG:
            warn("-- Method {0}.__init__".format(self, kwargs))
        super(Pyjo_IOLoop_Client, self).__init__(**kwargs)
        if self.reactor is None:
            self.reactor = Pyjo.IOLoop.singleton().reactor

    def __del__(self):
        if DEBUG:
            warn("-- Method {0}.__del__".format(self))

        self._cleanup()

    def connect(self, **kwargs):
        reactor = self.reactor
        timeout = kwargs.get('timeout', 10)

        # Timeout
        self = weakref.proxy(self)

        def timeout_cb(self):
            if dir(self):
                self.emit('error', 'Connect timeout')

        self._timer = reactor.timer(lambda: timeout_cb(self), timeout)

        # Blocking name resolution
        def resolved_cb(self):
            if dir(self):
                self._connect(**kwargs)

        return reactor.next_tick(lambda: resolved_cb(self))

    def start(self):
        def ready_cb(self):
            self._accept()
        self.reactor.io(lambda: ready_cb(self), self.handle)

    def stop(self):
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
            handle.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

            self.emit('accept', handle)
            # TODO TLS

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

            handle = socket.socket(AF_INET, SOCK_STREAM)
            handle.connect((address, port))
            # return self.emit('error', "Can't connect: " + str(e))
            self.handle = handle

        handle.setblocking(0)

        # Wait for handle to become writable
        self = weakref.proxy(self)

        def ready_cb(self, loop, **kwargs):
            if dir(self):
                self._ready(**kwargs)

        self.reactor.io(lambda loop: ready_cb(self, loop, **kwargs), handle).watch(handle, 0, 1)

    def _ready(self, **kwargs):
        # Retry or handle exceptions
        handle = self.handle

        # Disable Nagle's algorithm
        handle.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

        # TODO TLS, Socks
        return self._try_tls(**kwargs)

    def _port(self, **kwargs):
        port = kwargs.get('port')
        if not port:
            port = 80
        return port

    def _tls(self):
        handle = self.handle
        while True:
            try:
                handle.do_handshake()
                # Connected
                return self._cleanup().emit('connect', handle)
            except SSLWantReadError:
                return self.reactor.watch(handle, 1, 0)
            except SSLWantWriteError:
                return self.reactor.watch(handle, 1, 1)
            except SSLError:
                return self.reactor.watch(handle, 1, 1)
        return self.emit('error', 'TLS upgrade failed')

    def _try_tls(self, **kwargs):
        handle = self.handle
        if not kwargs.get('tls', False) or (TLS and isinstance(handle, ssl.SSLSocket)):
            return self._cleanup().emit('connect', handle)
        if not TLS:
            return self.emit('error', 'ssl required for TLS support')

        reactor = self.reactor
        reactor.remove(handle)
        try:
            ssl_handle = ssl.wrap_socket(handle, do_handshake_on_connect=False) # TODO options
            self.handle = ssl_handle
        except SSLError:
            return self.emit('error', 'TLS upgrade failed')
        reactor.io(lambda loop: self._tls(), ssl_handle).watch(ssl_handle, 0, 1)


new = Pyjo_IOLoop_Client.new
object = Pyjo_IOLoop_Client  # @ReservedAssignment
