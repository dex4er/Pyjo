"""
Pyjo.IOLoop
"""

import importlib
import weakref

import Pyjo.IOLoop.Client
import Pyjo.IOLoop.Server
import Pyjo.IOLoop.Stream
import Pyjo.Reactor

from Pyjo.Base import class_object
from Pyjo.Util import getenv, md5_sum, steady_time, rand, warn


DEBUG = getenv('PYJO_IOLOOP_DEBUG', 0)


class Error(Exception):
    pass


@class_object
class _(Pyjo.Base.object):
    accept_interval = 0.025
    lock = None
    unlock = None
    max_accepts = 0
    max_connections = 1000
    multi_accept = 50
    reactor = None

    _acceptors = {}
    _connections = {}

    _accept = None
    _accepts = None
    __stop = None
    __accepting = False

    def __init__(self):
        module = importlib.import_module(Pyjo.Reactor.detect())
        self.reactor = module.object()

        if DEBUG:
            warn("-- Reactor initialized ({0})".format(self.reactor))

        def cb(reactor, *args):
            raise Error(args)  # TODO debug
            warn("{0}: {1}".format(reactor, ": ".join(args)))

        # self.reactor.catch(cb)  # TODO

        return None

    def acceptor(self, acceptor):
        # Find acceptor for id
        if isinstance(acceptor, str):
            return self._acceptors[acceptor]

        # Connect acceptor with reactor
        cid = self._id()
        self._acceptors[cid] = acceptor
        if self.max_accepts:
            self._accepts = self.max_accepts

        # Allow new acceptor to get picked up
        self._not_accepting()

        return cid

    # TODO @classmethod
    def client(self, cb, **kwargs):
        # Make sure timers are running
        self._recurring()

        cid = self._id()
        client = Pyjo.IOLoop.Client.object()
        self._connections[cid] = {'client': client}
        client.reactor = weakref.proxy(self.reactor)

        self = weakref.proxy(self)

        def connect_cb(client, handle):
            if dir(self):
                del self._connections[cid]['client']
                stream = Pyjo.IOLoop.Stream.object(handle)
                self._stream(stream, cid)
                cb(self, None, stream)

        client.on('connect', connect_cb)

        # TODO client.on('error', error_cb)

        client.connect(**kwargs)
        return cid

    def recurring(self, after, cb):
        if DEBUG:
            warn("-- Recurring after {0} cb {1}".format(after, cb))
        return self._timer('recurring', after, cb)

    def remove(self, cid):
        c = self._connections[cid]
        if c:
            stream = c.stream
            if stream:
                return stream.close_gracefully()
        self._remove(cid)

    def is_running(self):
        return self.reactor.is_running()

    def server(self, cb, **kwargs):
        server = Pyjo.IOLoop.Server.object()

        def accept_cb(server, handle):
            stream = Pyjo.IOLoop.Stream.object(handle)
            cb(self, stream, self.stream(stream))

        server.on('accept', accept_cb)
        server.listen(**kwargs)

        return self.acceptor(server)

    def singleton(self):
        return loop

    def start(self):
        if self.is_running():
            raise Error('Pyjo.IOLoop already running')
        self.reactor.start()

    def stop(self):
        self.reactor.stop()

    def stream(self, stream):
        # Find stream for id
        if isinstance(stream, str):
            return self._connections[stream]

        # Release accept mutex
        self._not_accepting()

        # Enforce connection limit (randomize to improve load balancing)
        if self._accepts:
            self._accepts -= int(rand(2) + 1)
            if self._accepts <= 0:
                self.max_connections = 0

        return self._stream(stream, self._id())

    def timer(self, after, cb):
        return self._timer('timer', after, cb)

    def _accepting(self):
        # Check if we have acceptors
        if not self._acceptors:
            a = self._accept
            self._accept = None
            return self._remove(a)

        # Check connection limit
        i = len(self._connections)
        max_conns = self.max_connections
        if i >= max_conns:
            return

        # Acquire accept mutex
        if self.lock:
            self.lock(not i)

        a = self._accept
        self._accept = None
        self._remove(a)

        # Check if multi-accept is desirable
        multi = self.multi_accept
        for a in self._acceptors.itervalues():
            a.multi_accept = 1 if max_conns < multi else multi
            a.start()
        self.__accepting = True

    def _id(self):
        cid = None
        while True:
            cid = md5_sum('c{0}{1}'.format(steady_time(), rand()))
            if cid not in self._connections and cid not in self._acceptors:
                break
        return cid

    def _not_accepting(self):
        # Make sure timers are running
        self._recurring()

        # Release accept mutex
        if self.__accepting:
            self.__accepting = False
        else:
            return

        cb = self.unlock
        if not cb:
            return

        cb()

        for a in self._acceptors.itervalues():
            a.stop()

    def _recurring(self):
        if not self._accept:

            def cb_accepting(loop):
                loop._accepting()

            self._accept = self.recurring(self.accept_interval, cb_accepting)

        if not self.__stop:

            def cb_stop(loop):
                loop._stop()

            self.__stop = self.recurring(1, cb_stop)

    def _remove(self, _id):
        # Timer
        reactor = self.reactor

        if not reactor:
            return

        if reactor.remove(_id):
            return

        # Acceptor
        if _id in self._acceptors:
            del self._acceptors[_id]
            self._not_accepting()

        # Connections
        else:
            if _id in self._connections:
                del self._connections[_id]

    def _stop(self):
        if self._connections:
            return

        if self.max_connections == 0:
            self.stop()

        if self._acceptors:
            return

        if self._accept:
            self._remove(self._accept)
            self._accept = None

        if self.__stop:
            self._remove(self.__stop)
            self.__stop = None

    def _stream(self, stream, cid):
        # Make sure timers are running
        self._recurring()

        # Connect stream with reactor
        self._connections[cid] = {'stream': stream}
        stream.reactor = weakref.proxy(self.reactor)
        self = weakref.proxy(self)

        def close_cb(stream):
            if dir(self):
                self._remove(cid)

        stream.on('close', close_cb)
        stream.start()

        return cid

    def _timer(self, method, after, cb):
        self = weakref.proxy(self)
        return getattr(self.reactor, method)(after, lambda: cb(self))


loop = object()


def client(cb, **kwargs):
    return loop.client(cb, **kwargs)


def is_running():
    return loop.is_running()


def remove(cid):
    loop.remove(cid)


def server(cb, *args, **kwargs):
    return loop.server(cb, *args, **kwargs)


def singleton():
    return loop


def start():
    loop.start()


def stop():
    loop.stop()


def stream(stream):
    loop.stream(stream)


def timer(*args):
    loop.timer(*args)


def recurring(*args):
    loop.recurring(*args)
