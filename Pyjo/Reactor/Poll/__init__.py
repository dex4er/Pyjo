import os
import select
import socket
import time

import Pyjo.Reactor
from Pyjo.Util import md5_sum, rand, steady_time, warn


DEBUG = os.environ.get('PYJO_REACTOR_DEBUG', 1)


class object(Pyjo.Reactor.object):
    _running = False
    __poll = None
    _timers = {}
    _io = {}

    def again(self, tid):
        timer = self._timers[tid]
        timer['time'] = steady_time() + timer['after']

    def io(self, handle, cb):
        fd = handle.fileno()
        if not isinstance(fd, int):
            fd = fd.channel
        self._io[fd] = {'cb': cb}
        if DEBUG:
            warn("Reactor adding io[{0}] = {1}".format(fd, self._io[fd]))
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
            if not self._timers and not self._io:
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
            if self._io:
                events = poll.poll(timeout)
                for fd, flag in events:
                    if not isinstance(fd, int):
                        fd = fd.fileno().channel
                    if flag & (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR):
                        io = self._io[fd]
                        i += 1
                        self._sandbox('Read', io['cb'], 0)
                    elif flag & (select.POLLOUT):
                        io = self._io[fd]
                        i += 1
                        self._sandbox('Write', io['cb'], 1)

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
                        warn("Timer {0} = {1}".format(tid, t))
                    self._sandbox("Timer {0}".format(tid), t['cb'])

        # Restore state if necessary
        if self._running:
            self._running = running

    def recurring(self, *args, **kwargs):
        return self._timer(True, *args, **kwargs)

    def remove(self, remove):
        if remove is None:
            raise RuntimeWarning("Reactor remove None")

        if isinstance(remove, str):
            if DEBUG:
                warn("Reactor remove timer[{0}]".format(remove))
            if remove in self._timers:
                timer = self._timers[remove]
                del self._timers[remove]
                return True
            return False

        try:
            fd = remove.fileno()
            if not isinstance(fd, int):
                fd = fd.channel
            if DEBUG:
                warn("Reactor remove io[{0}]".format(fd))
            self._poll().unregister(remove)
            if remove.fileno() in self._io:
                io = self._io[fd]
                del self._io[fd]
                return True
            remove.close()
        except socket.error:
            if DEBUG:
                warn("Reactor remove io {0} but is already closed".format(remove))
            pass
        return False

    def start(self):
        self._running = True
        while self._running:
            self.one_tick()

    def stop(self):
        self._running = False

    def timer(self, *args, **kwargs):
        return self._timer(False, *args, **kwargs)

    def watch(self, handle, read, write):
        poll = self._poll()
        # TODO poll.unregister(handle)
        if read and write:
            poll.register(handle, select.POLLIN | select.POLLPRI | select.POLLOUT)
        elif read:
            poll.register(handle, select.POLLIN | select.POLLPRI)
        elif write:
            poll.register(handle, select.POLLOUT)
        return self

    def _poll(self):
        if not self.__poll:
            self.__poll = select.poll()
        return self.__poll

    def _sandbox(self, event, cb, *args):
        cb(*args)
        """
        try:
            cb(*args)
        except Exception as e:
            self.emit('error', "{0} failed: {1}".format(event, e))
        """

    def _timer(self, recurring, after, cb):
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
            warn("Reactor adding timer[{0}] = {1}".format(tid, self._timers[tid]))

        return tid
