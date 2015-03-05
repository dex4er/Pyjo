"""
Pyjo.IOLoop.Delay - Manage callbacks and control the flow of events
===================================================================
::

    import Pyjo.IOLoop

    # Synchronize multiple events
    delay = Pyjo.IOLoop.delay()

    @delay.step
    def step(delay):
        print('BOOM!')

    for i in range(10):
        end = delay.begin()

        def timer_wrap(i):
            def timer_cb(loop):
                print(10 - i)
                end()
            return timer_cb

        Pyjo.IOLoop.timer(timer_wrap(i), i)

    delay.wait()

    # Sequentialize multiple events
    delay = Pyjo.IOLoop.delay()

    @delay.step
    def step1(delay):
        # First step (simple timer)
        Pyjo.IOLoop.timer(delay.begin(), 2)
        print('Second step in 2 seconds.')

    @delay.step
    def step2(delay):
        # Second step (concurrent timers)
        Pyjo.IOLoop.timer(delay.begin(), 1)
        Pyjo.IOLoop.timer(delay.begin(), 3)
        print('Third step in 3 seconds.')

    @delay.step
    def step3(delay):
        print('And done after 5 seconds total.')

    delay.wait()

    # Handle exceptions in all steps
    delay = Pyjo.IOLoop.delay()

    @delay.step
    def step1(delay):
        raise Exception('Intentional error')

    @delay.step
    def step2(delay):
        print('Never actually reached.')

    @delay.catch
    def step3(delay, err):
        print("Something went wrong: {0}".format(err))

    delay.wait()
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Base import lazy


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
            self.ioloop = Pyjo.IOLoop.singleton

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

    def step(self, cb):
        remaining = self.remaining()
        remaining.append(cb)
        return self

    def steps(self, *args):
        return self.remaining(*args)

    def wait(self):
        self.ioloop.next_tick(self.begin())
        if self.ioloop.is_running:
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
