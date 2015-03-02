"""
Pyjo.Reactor.Poll - Low-level event reactor with poll support
=============================================================
::

    import Pyjo.Reactor.Poll

    # Watch if handle becomes readable or writable
    reactor = Pyjo.Reactor.Poll.new()

    def io_cb(reactor, writable):
        if writable:
            print('Handle is writable')
        else:
            print('Handle is readable')

    reactor.io(io_cb, handle)

    # Change to watching only if handle becomes writable
    reactor.watch(handle, read=False, write=True)

    # Add a timer
    def timer_cb(reactor):
        reactor.remove(handle)
        print('Timeout!')

    reactor.timer(timer_cb, 15)

    # Start reactor if necessary
    if not reactor.is_running:
        reactor.start()

:mod:`Pyjo.Reactor.Poll` is a low-level event reactor based on :meth:`select.poll`.

Events
------

:mod:`Pyjo.Reactor.Poll` inherits all events from :mod:`Pyjo.Reactor.Select`.

Classes
-------
"""

import Pyjo.Reactor.Select

from Pyjo.Base import lazy
from Pyjo.Util import getenv, steady_time, warn

import select
import socket
import time


DEBUG = getenv('PYJO_REACTOR_DEBUG', False)


class Pyjo_Reactor_Poll(Pyjo.Reactor.Select.object):
    """
    :mod:`Pyjo.Reactor.Poll` inherits all attributes and methods from
    :mod:`Pyjo.Reactor.Select` and implements the following new ones.
    """

    _running = False
    _select_poll = None
    _timers = lazy(lambda self: {})
    _ios = lazy(lambda self: {})

    def is_readable(self, handle):
        """::

            boolean = reactor.is_readable(handle)

        Quick non-blocking check if a handle is readable.
        """
        p = select.poll()
        p.register(handle.fileno(), select.POLLIN | select.POLLPRI)
        return bool(p.poll(0))

    def one_tick(self):
        """::

            reactor.one_tick()

        Run reactor until an event occurs. Note that this method can recurse back into
        the reactor, so you need to be careful. Meant to be overloaded in a subclass.
        """
        # Remember state for later
        running = self._running
        self._running = True

        poll = self._poll()

        # Wait for one event
        last = False
        while not last:
            # Stop automatically if there is nothing to watch
            if not self._timers and not self._ios:
                return self.stop()

            # Calculate ideal timeout based on timers
            times = [t['time'] for t in self._timers.values()]
            if times:
                timeout = min(times) - steady_time()
            else:
                timeout = 0.5

            if timeout < 0:
                timeout = 0

            # I/O
            if self._ios:
                events = poll.poll(timeout * 1000)
                for fd, flag in events:
                    if fd in self._ios:
                        if flag & (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR):
                            io = self._ios[fd]
                            last = True
                            self._sandbox(io['cb'], 'Read', False)
                        if flag & (select.POLLOUT):
                            io = self._ios[fd]
                            last = True
                            self._sandbox(io['cb'], 'Write', True)

            # Wait for timeout if poll can't be used
            elif timeout:
                time.sleep(timeout)

            # Timers (time should not change in between timers)
            now = steady_time()
            for tid in list(self._timers):
                t = self._timers.get(tid)

                if not t or t['time'] > now:
                    continue

                # Recurring timer
                if 'recurring' in t:
                    t['time'] = now + t['recurring']

                # Normal timer
                else:
                    self.remove(tid)

                last = True
                if t['cb']:
                    if DEBUG:
                        warn("-- Alarm timer[{0}] = {1}".format(tid, t))
                    self._sandbox(t['cb'], "Timer {0}".format(tid))

        # Restore state if necessary
        if self._running:
            self._running = running

    def remove(self, remove):
        """::

            boolean = reactor.remove(handle)
            boolean = reactor.remove(tid)

        Remove handle or timer.
        """
        if remove is None:
            if DEBUG:
                warn("-- Reactor remove None")
            return

        if isinstance(remove, str):
            if DEBUG:
                if remove in self._timers:
                    warn("-- Reactor remove timer[{0}] = {1}".format(remove, self._timers[remove]))
                else:
                    warn("-- Reactor remove timer[{0}] = None".format(remove))
            if remove in self._timers:
                del self._timers[remove]
                return True

            return False

        try:
            fd = remove.fileno()
            if DEBUG:
                if fd in self._ios:
                    warn("-- Reactor remove io[{0}]".format(fd))
            poll = self._poll()
            if poll:
                poll.unregister(remove)
            if fd in self._ios:
                del self._ios[fd]
                return True
            # remove.close()  # TODO remove?
        except socket.error:
            if DEBUG:
                warn("-- Reactor remove io {0} already closed".format(remove))
            pass

        return False

    def reset(self):
        """::

            reactor.reset()

        Remove all handles and timers.
        """
        self._ios = {}
        self._select_poll = None
        self._timers = {}

    def watch(self, handle, read, write):
        """::

            reactor = reactor.watch(handle, read, write)

        Change I/O events to watch handle for with true and false values. Meant to be
        overloaded in a subclass. Note that this method requires an active I/O
        watcher.
        """
        mode = 0
        if read:
            mode |= select.POLLIN | select.POLLPRI
        if write:
            mode |= select.POLLOUT

        poll = self._poll()
        poll.register(handle, mode)

        return self

    def _poll(self):
        if not self._select_poll:
            self._select_poll = select.poll()

        return self._select_poll


new = Pyjo_Reactor_Poll.new
object = Pyjo_Reactor_Poll  # @ReservedAssignment
