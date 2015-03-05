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

:mod:`Pyjo.IOLoop.Delay` manages callbacks and controls the flow of events for
:mod:`Pyjo.IOLoop`, which can help you avoid deep nested closures and memory
leaks that often result from continuation-passing style.

Events
------

:mod:`Pyjo.IOLoop.Delay` inherits all events from :mod:`Pyjo.EventEmitter` and can
emit the following new ones.

error
~~~~~
::

    @delay.on
    def error(delay, err):
        ...

Emitted if an exception gets thrown in one of the steps, breaking the chain,
fatal if unhandled.

finish
~~~~~~
::

    @delay.on
    def finish(delay, *args):
        ...

Emitted once the active event counter reaches zero and there are no more
steps.

Classes
-------
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Base import lazy


REMAINING = {}


class Pyjo_IOLoop_Delay(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.IOLoop.Delay` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    ioloop = lazy(lambda self: Pyjo.IOLoop.singleton)
    """::

        ioloop = delay.ioloop
        delay.ioloop = Pyjo.IOLoop.new()

    Event loop object to control, defaults to the global :mod:`Pyjo.IOLoop`
    singleton.
    """

    _counter = 0
    _pending = 0
    _lock = False
    _fail = False

    _data = lazy(lambda self: {})
    _args = lazy(lambda self: [])

    def begin(self, offset=1, length=0, *args):
        """::

            cb = delay.begin
            cb = delay.begin(offset)
            cb = delay.begin(offset, length)

        Indicate an active event by incrementing the active event counter, the
        returned callback needs to be called when the event has completed, to
        decrement the active event counter again. When all callbacks have been called
        and the active event counter reached zero, :meth:`steps` will continue. ::

            # Capture all arguments except for the first one (invocant)
            delay = Pyjo.IOLoop.delay()

            @delay.step
            def step1(delay, err, stream):
                ...

            Pyjo.IOLoop.client(delay.begin(), port=3000)
            delay.wait()

        Arguments passed to the returned callback are sliced with the given offset
        and length, defaulting to an offset of ``1`` with no default length. The
        arguments are then combined in the same order :meth:`begin` was called, and
        passed together to the next step or ``finish`` event. ::

            # Capture all arguments
            delay = Pyjo.IOLoop.delay()

            @delay.step
            def step2(delay, loop, err, stream):
                ...

            Pyjo.IOLoop.client(delay.begin(0), port=3000)
            delay.wait()

            # Capture only the second argument
            delay = Pyjo.IOLoop.delay()

            @delay.step
            def step3(delay, err):
                ...

            Pyjo.IOLoop.client(delay.begin(1, 1), port=3000)
            delay.wait()

            # Capture and combine arguments
            delay = Pyjo.IOLoop.delay()

            @delay.step
            def step4(delay, three_err, three_stream, four_err, four_stream):
                ...

            Pyjo.IOLoop.client(delay.begin(), port=3000)
            Pyjo.IOLoop.client(delay.begin(), port=4000)
            delay.wait()
        """
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

    def remaining(self, steps=None):
        if steps is None:
            if self not in REMAINING:
                REMAINING[self] = []
            return REMAINING[self]
        else:
            if len(steps):
                REMAINING[self] = steps
            elif self in REMAINING:
                del REMAINING[self]
            return self

    def step(self, cb):
        remaining = self.remaining()
        remaining.append(cb)
        return self

    def steps(self, *args):
        remaining = self.remaining()
        remaining.extend(args)
        return self

    def wait(self):
        self.ioloop.next_tick(self.begin())
        if self.ioloop.is_running:
            return
        self.once(lambda self, *args: self._die(*args), 'error')
        self.once(lambda self, *args: self.ioloop.stop(), 'finish')
        self.ioloop.start()

    def _die(self, err):
        if self.has_subscribers('error'):
            self.ioloop.stop()
        else:
            raise Exception(err)

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
            try:
                cb(self, *args)
            except Exception as ex:
                self._fail = True
                self.remaining([]).emit('error', ex)

        if not self._counter:
            return self.remaining([]).emit('finish', *args)

        if not self._pending:
            self.ioloop.next_tick(self.begin())

        return self


new = Pyjo_IOLoop_Delay.new
object = Pyjo_IOLoop_Delay  # @ReservedAssignment
