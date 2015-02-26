"""
Pyjo.IOLoop
"""

import importlib
import weakref

import Pyjo.Base
import Pyjo.IOLoop.Client
import Pyjo.IOLoop.Delay
import Pyjo.IOLoop.Server
import Pyjo.IOLoop.Stream
import Pyjo.Reactor

from Pyjo.Base import lazy
from Pyjo.Util import (
    decorator, decoratormethod, getenv, md5_sum, steady_time, rand,
    warn
)


DEBUG = getenv('PYJO_IOLOOP_DEBUG', 0)


class Error(Exception):
    pass


class Pyjo_IOLoop(Pyjo.Base.object):

    accept_interval = 0.025
    lock = None
    unlock = None
    max_accepts = 0
    max_connections = 1000
    multi_accept = 50
    reactor = None

    _acceptors = lazy(lambda self: {})
    _connections = lazy(lambda self: {})

    _accepts = 0
    _accept_timer = None
    _stop_timer = None
    _accepting_timer = None

    def __init__(self, **kwargs):
        super(Pyjo_IOLoop, self).__init__(**kwargs)

        # TODO Pyjo.Loader
        module = importlib.import_module(Pyjo.Reactor.detect())
        module_class_name = module.__name__.replace('.', '_')
        module_class = getattr(module, module_class_name)
        self.reactor = module_class()

        if DEBUG:
            warn("-- Reactor initialized ({0})".format(self.reactor))

        def error_cb(reactor, *args):
            raise Error(args)  # TODO debug
            warn("{0}: {1}".format(reactor, ": ".join(args)))

        # self.reactor.catch(error_cb)  # TODO

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

    def client(self, cb=None, **kwargs):
        if cb is None:
            def wrap(func):
                return self.client(func, **kwargs)
            return wrap

        # Make sure timers are running
        self._recurring()

        cid = self._id()
        client = Pyjo.IOLoop.Client.new()
        self._connections[cid] = {'client': client}
        client.reactor = weakref.proxy(self.reactor)

        self = weakref.proxy(self)

        def connect_cb(self, cid, client, handle):
            if dir(self):
                del self._connections[cid]['client']
                stream = Pyjo.IOLoop.Stream.new(handle)
                self._stream(stream, cid)
                cb(self, None, stream)

        client.on(lambda client, handle: connect_cb(self, cid, client, handle), 'connect')

        # TODO client.on(error_cb, 'error')

        client.connect(**kwargs)
        return cid

    def delay(self, *args):
        delay = Pyjo.IOLoop.Delay.new()
        delay.ioloop = weakref.proxy(self)
        if args:
            return delay.steps(*args)
        else:
            return delay

    @property
    def is_running(self):
        return self.reactor.is_running

    @decoratormethod
    def next_tick(self, cb):
        return self.reactor.next_tick(cb)

    def one_tick(self):
        return self.reactor.one_tick()

    @decoratormethod
    def recurring(self, cb, after):
        if DEBUG:
            warn("-- Recurring after {0} cb {1}".format(after, cb))
        return self._timer(cb, 'recurring', after)

    def remove(self, taskid):
        if taskid in self._connections:
            c = self._connections[taskid]
            if c:
                stream = c.get('stream')
                if stream:
                    return stream.close_gracefully()

        self._remove(taskid)

    def server(self, cb=None, **kwargs):
        if cb is None:
            def wrap(func):
                return self.server(func, **kwargs)
            return wrap

        server = Pyjo.IOLoop.Server.new()

        def accept_cb(self, server, handle):
            stream = Pyjo.IOLoop.Stream.new(handle)
            cb(self, stream, self.stream(stream))

        server.on(lambda server, handle: accept_cb(self, server, handle), 'accept')
        server.listen(**kwargs)

        return self.acceptor(server)

    @classmethod
    def singleton(self):
        return instance

    def start(self):
        if self.is_running:
            raise Error('Pyjo.IOLoop already running')
        self.reactor.start()

    def stop(self):
        self.reactor.stop()

    def stream(self, stream):
        # Find stream for id
        if isinstance(stream, str):
            return self._connections[stream]['stream']

        # Release accept mutex
        self._not_accepting()

        # Enforce connection limit (randomize to improve load balancing)
        if self._accepts:
            self._accepts -= int(rand(2) + 1)
            if self._accepts <= 0:
                self.max_connections = 0

        return self._stream(stream, self._id())

    @decoratormethod
    def timer(self, cb, after):
        if DEBUG:
            warn("-- Timer after {0} cb {1}".format(after, cb))
        return self._timer(cb, 'timer', after)

    def _accepting(self):
        # Check if we have acceptors
        if not self._acceptors:
            a = self._accept_timer
            self._accept_timer = None
            return self._remove(a)

        # Check connection limit
        i = len(self._connections)
        max_conns = self.max_connections
        if i >= max_conns:
            return

        # Acquire accept mutex
        if self.lock:
            self.lock(not i)

        a = self._accept_timer
        self._accept_timer = None
        self._remove(a)

        # Check if multi-accept is desirable
        multi = self.multi_accept
        for a in self._acceptors.values():
            a.multi_accept = 1 if max_conns < multi else multi
            a.start()
        self._accepting_timer = True

    def _id(self):
        taskid = None
        while True:
            taskid = md5_sum('c{0}{1}'.format(steady_time(), rand()).encode('ascii'))
            if taskid not in self._connections and taskid not in self._acceptors:
                break
        return taskid

    def _not_accepting(self):
        # Make sure timers are running
        self._recurring()

        # Release accept mutex
        if self._accepting_timer:
            self._accepting_timer = False
        else:
            return

        cb = self.unlock
        if not cb:
            return

        cb()

        for a in self._acceptors.itervalues():
            a.stop()

    def _recurring(self):
        if not self._accept_timer:

            def accept_timer_cb(loop):
                loop._accepting()

            self._accept_timer = self.recurring(accept_timer_cb, self.accept_interval)

        if not self._stop_timer:

            def stop_timer_cb(loop):
                loop._stop()

            self._stop_timer = self.recurring(stop_timer_cb, 1)

    def _remove(self, taskid):
        # Timer
        reactor = self.reactor

        if not reactor:
            return

        if reactor.remove(taskid):
            return

        # Acceptor
        if taskid in self._acceptors:
            self._acceptors[taskid].stop()
            del self._acceptors[taskid]
            self._not_accepting()

        # Connections
        else:
            if taskid in self._connections:
                del self._connections[taskid]

    def _stop(self):
        if self._connections:
            return

        if self.max_connections == 0:
            self.stop()

        if self._acceptors:
            return

        if self._accept_timer:
            self._remove(self._accept_timer)
            self._accept_timer = None

        if self._stop_timer:
            self._remove(self._stop_timer)
            self._stop_timer = None

    def _stream(self, stream, cid):
        # Make sure timers are running
        self._recurring()

        # Connect stream with reactor
        self._connections[cid] = {'stream': stream}
        stream.reactor = weakref.proxy(self.reactor)
        self = weakref.proxy(self)

        def on_close_cb(self, stream):
            if dir(self):
                self._remove(cid)

        stream.on(lambda stream: on_close_cb(self, stream), 'close')
        stream.start()

        return cid

    def _timer(self, cb, method, after):
        self = weakref.proxy(self)
        return getattr(self.reactor, method)(lambda: cb(self), after)


def new(*args, **kwargs):
    return Pyjo_IOLoop(*args, **kwargs)


instance = Pyjo_IOLoop()


def acceptor(acceptor):
    return instance.acceptor(acceptor)


def client(cb=None, **kwargs):
    if cb is None:
        def wrap(func):
            return instance.client(func, **kwargs)
        return wrap

    return instance.client(cb, **kwargs)


def delay(*args):
    return instance.delay(*args)


def is_running():
    return instance.is_running


@decorator
def next_tick(cb):
    return instance.next_tick(cb)


def one_tick():
    return instance.one_tick()


@decorator
def recurring(cb, after):
    return instance.recurring(cb, after)


def remove(taskid):
    return instance.remove(taskid)


def server(cb=None, **kwargs):
    if cb is None:
        def wrap(func):
            return instance.server(func, **kwargs)
        return wrap

    return instance.server(cb, **kwargs)


def singleton():
    return instance


def start():
    return instance.start()


def stop():
    return instance.stop()


def stream(stream):
    return instance.stream(stream)


@decorator
def timer(cb, after=None):
    return instance.timer(cb, after)


new = Pyjo_IOLoop.new
object = Pyjo_IOLoop  # @ReservedAssignment
