"""
Pyjo.IOLoop.Client
"""

import socket
import weakref

from socket import AF_INET, IPPROTO_TCP, TCP_NODELAY, SOCK_STREAM

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Util import getenv, lazy, warn


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

        self._timer = reactor.timer(timeout, lambda: timeout_cb(self))

        # Blocking name resolution
        def resolved_cb(self):
            if dir(self):
                self._connect(**kwargs)

        return reactor.next_tick(lambda: resolved_cb(self))

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

        self.reactor.io(handle, lambda loop: ready_cb(self, loop, **kwargs)).watch(handle, 0, 1)

    def _ready(self, **kwargs):
        # Retry or handle exceptions
        handle = self.handle

        # Disable Nagle's algorithm
        handle.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

        # TODO TLS, Socks
        return self._cleanup().emit('connect', handle)

    def _port(self, **kwargs):
        port = kwargs.get('port')
        if not port:
            port = 80
        return port

    def start(self):
        def ready_cb(self):
            self._accept()
        self.reactor.io(self.handle, lambda: ready_cb(self))

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


new = Pyjo_IOLoop_Client.new
object = Pyjo_IOLoop_Client  # @ReservedAssignment
