"""
Pyjo.IOLoop.Client
"""

from socket import AF_INET, IPPROTO_TCP, TCP_NODELAY, SOCK_STREAM
import socket
import weakref

import Pyjo.EventEmitter
import Pyjo.IOLoop
from Pyjo.Util import getenv, warn


DEBUG = getenv('PYJO_IOLOOP_CLIENT_DEBUG', 0)


class object(Pyjo.EventEmitter.object):
    reactor = None
    handle = None

    _timer = None

    def __init__(self):
        if DEBUG:
            warn("-- Method {0}.__init__".format(self))
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
        def timeout_cb():
            if dir(self):
                self.emit('error', 'Connect timeout')

        self._timer = reactor.timer(timeout, timeout_cb)

        # Blocking name resolution
        def resolved_cb():
            if dir(self):
                self._connect(**kwargs)

        return reactor.next_tick(resolved_cb)

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

        def ready_cb(loop):
            if dir(self):
                self._ready(**kwargs)

        self.reactor.io(handle, ready_cb).watch(handle, 0, 1)

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
        def ready_cb():
            self._accept()
        self.reactor.io(self.handle, ready_cb)

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
