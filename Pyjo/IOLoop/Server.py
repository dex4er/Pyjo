"""
Pyjo.IOLoop.Server
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Base import lazy

import socket
import weakref


class Pyjo_IOLoop_Server(Pyjo.EventEmitter.object):

    reactor = lazy(lambda self: Pyjo.IOLoop.singleton.reactor)
    multi_accept = 50
    handle = None

    _handles = lazy(lambda self: {})

    def __del__(self):
        if dir(self.reactor):
            if dir(self.handle) and self.handle:
                self.stop()
            for handle in self._handles.values():
                self.reactor.remove(handle)

    def generate_port(self):
        listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen.bind(('127.0.0.1', 0))
        listen.listen(5)
        return listen.getsockname()[1]

    def listen(self, **kwargs):
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
        self.handle = s

    @property
    def port(self):
        return self.handle.getsockname()[1]

    def start(self):
        def ready_cb(self, unused):
            self._accept()
        self = weakref.proxy(self)
        self.reactor.io(lambda reactor, write: ready_cb(self, reactor), self.handle)

    def stop(self):
        self.reactor.remove(self.handle)
        self.handle = None

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
            # self.reactor.remove(self.handle)
            # TODO TLS


new = Pyjo_IOLoop_Server.new
object = Pyjo_IOLoop_Server  # @ReservedAssignment
