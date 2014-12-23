"""
Pyjo.IOLoop.Delay
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Util import lazy


REMAINING = {}


class Pyjo_IOLoop_Delay(Pyjo.EventEmitter.object):

    ioloop = None

    _counter = 0
    _pending = 0
    _lock = False
    _fail = False

    _data = lazy(lambda self: {})
    _args = lazy(lambda self: [])

    def __init__(self, **kwargs):
        super(Pyjo_IOLoop_Delay, self).__init__(**kwargs)
        if self.ioloop is None:
            self.ioloop = Pyjo.IOLoop.singleton()

    def begin(self, offset=1, length=0, *args):
        self._pending += 1
        self._counter += 1
        sid = self._counter
        return lambda *args: self._step(sid, offset, length, *args)

    def data(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._data = args[0]
            return self._data
        if kwargs:
            self._data = kwargs
            return self._data
        if len(args) == 2:
            self._data[args[0]] = self._data[args[1]]
            return self
        if len(args) == 1:
            return self._data[args[0]]
        return self._data

    def next(self, *args):
        self.begin()(self, *args)

    def remaining(self, *args):
        if not args:
            if self not in REMAINING:
                REMAINING[self] = []
            return REMAINING[self]
        REMAINING[self] = list(args)
        return self

    def steps(self, *args):
        self = self.remaining(*args)
        self.ioloop.next_tick(self.begin())
        return self

    def wait(self):
        if self.ioloop.is_running():
            return
        # TODO once error
        self.once(lambda e, *args: self.ioloop.stop(), 'finish')
        self.ioloop.start()

    def _step(self, sid, offset=1, length=0, *args):
        if args:
            if length:
                args = args[offset: offset + length]
            else:
                args = args[offset:]
        if sid >= len(self._args):
            self._args.append(args)
        else:
            self._args[sid] = args

        if self._fail:
            return self
        self._pending -= 1
        if self._pending:
            return self
        if self._lock:
            return self

        args = [item for sublist in self._args for item in sublist]
        self._args = []

        self._counter = 0
        remaining = self.remaining()
        if len(remaining):
            cb = remaining.pop(0)
            # TODO try
            cb(self, *args)
            # TODO catch e: self._fail += 1; self.remaining([]).emit('error', e)
        if not self._counter:
            return self.remaining([]).emit('finish', *args)
        if not self._pending:
            self.ioloop.next_tick(self.begin())
        return self


new = Pyjo_IOLoop_Delay.new
object = Pyjo_IOLoop_Delay  # @ReservedAssignment
