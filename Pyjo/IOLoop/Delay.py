"""
Pyjo.IOLoop.Delay
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop


REMAINING = {}


class Pyjo_IOLoop_Delay(Pyjo.EventEmitter.object):
    def __init__(self):
        self.ioloop = Pyjo.IOLoop.singleton()
        self._data = {}

        self._counter = 0
        self._pending = 0
        self._lock = False
        self._fail = False
        self._args = []

        super(Pyjo_IOLoop_Delay, self).__init__()

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
        self.once('finish', lambda e, *args: self.ioloop.stop())
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


def new(*args, **kwargs):
    return Pyjo_IOLoop_Delay(*args, **kwargs)


object = Pyjo_IOLoop_Delay  # @ReservedAssignment
