"""
Pyjo.Reactor.Poll
"""

import select
import socket
import time

from select import POLLERR, POLLHUP, POLLIN, POLLOUT, POLLPRI

import Pyjo.Reactor.Select

from Pyjo.Base import lazy
from Pyjo.Util import getenv, steady_time, warn


DEBUG = getenv('PYJO_REACTOR_DEBUG', 0)


class Pyjo_Reactor_Poll(Pyjo.Reactor.Select.object):

    _running = False
    _select_poll = None
    _timers = lazy(lambda self: {})
    _ios = lazy(lambda self: {})

    def is_readable(self, handle):
        p = select.poll()
        p.register(handle.fileno(), select.POLLIN | select.POLLPRI)
        return bool(p.poll(0))

    def one_tick(self):
        # Remember state for later
        running = self._running
        self._running = True

        # Wait for one event
        i = 0
        poll = self._poll()
        while not i:
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
                    if flag & (POLLIN | POLLPRI | POLLHUP | POLLERR):
                        io = self._ios[fd]
                        i += 1
                        self._sandbox(io['cb'], 'Read', 0)
                    elif flag & (POLLOUT):
                        io = self._ios[fd]
                        i += 1
                        self._sandbox(io['cb'], 'Write', 1)

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

                i += 1
                if t['cb']:
                    if DEBUG:
                        warn("-- Alarm timer[{0}] = {1}".format(tid, t))
                    self._sandbox(t['cb'], "Timer {0}".format(tid))

        # Restore state if necessary
        if self._running:
            self._running = running

    def remove(self, remove):
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
        self._ios = {}
        self._select_poll = None
        self._timers = {}

    def watch(self, handle, read, write):
        mode = 0
        if read:
            mode |= POLLIN | POLLPRI
        if write:
            mode |= POLLOUT

        poll = self._poll()
        poll.register(handle, mode)

        return self

    def _poll(self):
        if not self._select_poll:
            self._select_poll = select.poll()
        return self._select_poll

new = Pyjo_Reactor_Poll.new
object = Pyjo_Reactor_Poll  # @ReservedAssignment
