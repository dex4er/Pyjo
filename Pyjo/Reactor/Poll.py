"""
Pyjo.Reactor.Poll
"""

import select
import socket
import time

from select import POLLERR, POLLHUP, POLLIN, POLLOUT, POLLPRI

import Pyjo.Reactor

from Pyjo.Util import getenv, lazy, md5_sum, rand, steady_time, warn


DEBUG = getenv('PYJO_REACTOR_DEBUG', 0)


class Pyjo_Reactor_Poll(Pyjo.Reactor.object):

    _running = False
    _select_poll = None
    _timers = lazy(lambda: {})
    _ios = lazy(lambda: {})

    def again(self, tid):
        timer = self._timers[tid]
        timer['time'] = steady_time() + timer['after']

    def io(self, cb, handle):
        fd = handle.fileno()
        if fd in self._ios:
            self._ios[fd]['cb'] = cb
            if DEBUG:
                warn("-- Reactor found io[{0}] = {1}".format(fd, self._ios[fd]))
        else:
            self._ios[fd] = {'cb': cb}
            if DEBUG:
                warn("-- Reactor adding io[{0}] = {1}".format(fd, self._ios[fd]))
        return self.watch(handle, 1, 1)

    def is_running(self):
        return self._running

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

    def recurring(self, cb, after):
        return self._timer(cb, True, after)

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

    def start(self):
        self._running = True
        while self._running:
            self.one_tick()

    def stop(self):
        self._running = False

    def timer(self, cb, after):
        return self._timer(cb, False, after)

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

    def _sandbox(self, cb, event, *args):
        cb(*args)
        """
        try:
            cb(*args)
        except Exception as e:
            self.emit('error', "{0} failed: {1}".format(event, e))
        """

    def _timer(self, cb, recurring, after):
        tid = None
        while True:
            tid = md5_sum('t{0}{1}'.format(steady_time(), rand()))
            if tid not in self._timers:
                break

        timer = {'cb': cb, 'after': after, 'time': steady_time() + after}
        if recurring:
            timer['recurring'] = after
        self._timers[tid] = timer

        if DEBUG:
            warn("-- Reactor adding timer[{0}] = {1}".format(tid, self._timers[tid]))

        return tid


new = Pyjo_Reactor_Poll.new
object = Pyjo_Reactor_Poll  # @ReservedAssignment
