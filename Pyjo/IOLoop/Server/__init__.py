import socket

import Pyjo.EventEmmiter
import Pyjo.IOLoop


class object(Pyjo.EventEmmiter.object):
    multi_accept = 50
    reactor = None
    handle = None

    def __init__(self):
        self.reactor = Pyjo.IOLoop.singleton().reactor

    def listen(self, **kwargs):
        address = kwargs.get('address', '127.0.0.1')
        port = kwargs.get('port', 0)
        backlog = kwargs.get('backlog', socket.SOMAXCONN)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((address, port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(0)
        s.listen(backlog)
        self.handle = s

    def start(self):
        self.reactor.io(self.handle, lambda(loop): self._accept())

    def stop(self):
        self.reactor.remove(self.handle)

    def _accept(self):
        # Greedy accept
        for _ in range(0, self.multi_accept):
            print("before accept")
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
            # TODO TLS
