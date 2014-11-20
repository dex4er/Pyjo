from socket import AF_INET, IPPROTO_TCP, TCP_NODELAY, SOCK_STREAM
import socket

import Pyjo.EventEmmiter
import Pyjo.IOLoop


class object(Pyjo.EventEmmiter.object):
    reactor = None
    handle = None

    _timer = None

    def __init__(self):
        self.reactor = Pyjo.IOLoop.singleton().reactor

    def connect(self, **kwargs):
        reactor = self.reactor
        timeout = kwargs.get('timeout', 10)

        # Timeout
        # weaken self
        def timeout_cb():
            self.emit('error', 'Connect timeout')

        self._timer = reactor.timer(timeout, timeout_cb)

        # Blocking name resolution
        def resolved_cb():
            if self:
                self._connect(**kwargs)

        return reactor.next_tick(resolved_cb)

    def _cleanup(self):
        reactor = self.reactor

        if not reactor:
            return

        if self._timer:
            self._timer = None

        if self.handle:
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
        # weaken self
        self.reactor.io(handle, lambda(loop): self._ready(**kwargs)).watch(handle, 0, 1)

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
        self.reactor.io(self.handle, lambda(loop): self._accept())

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
