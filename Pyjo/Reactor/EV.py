"""
Pyjo.Reactor.EV
"""

import pyev
import weakref

import Pyjo.Reactor.Select

from Pyjo.Util import lazy


class Pyjo_Reactor_EV(Pyjo.Reactor.Select.object):

    _loop = lazy(lambda: pyev.default_loop())

    def again(self, tid):
        self._timers[tid]['watcher'].reset()

    def is_running(self):
        return self._loop.depth

    def one_tick(self):
        self._loop.start(pyev.EVRUN_ONCE)

    def recurring(self, cb, after):
        return self._timer(cb, True, after)

    def remove(self, remove):
        if isinstance(remove, str):
            if remove in self._timers:
                if 'watcher' in self._timers[remove]:
                    self._timers[remove]['watcher'].stop()
                    del self._timers[remove]['watcher']
        else:
            fd = remove.fileno()
            if fd in self._ios:
                if 'watcher' in self._ios[fd]:
                    self._ios[fd]['watcher'].stop()
                    del self._ios[fd]['watcher']

        super(Pyjo_Reactor_EV, self).remove(remove)

    def start(self):
        self._loop.start()

    def stop(self):
        self._loop.stop(pyev.EVBREAK_ALL)

    def timer(self, cb, after):
        return self._timer(cb, False, after)

    def watch(self, handle, read, write):
        mode = 0

        if read:
            mode |= pyev.EV_READ
        if write:
            mode |= pyev.EV_WRITE

        fd = handle.fileno()
        if fd not in self._ios:
            self._ios[fd] = {}
        io = self._ios[fd]

        if mode == 0:
            if 'watcher' in io:
                io['watcher'].stop()
                del io['watcher']
        else:
            if 'watcher' in io:
                w = io['watcher']
                w.stop()
                w.set(fd, mode)  # TODO Exception pyev.Error: 'cannot set a watcher while it is active'
                w.start()
            else:
                self = weakref.proxy(self)

                watcher = self._loop.io(fd, mode,
                                        lambda watcher, revents:
                                        self._io(watcher, fd, revents))
                watcher.start()
                io['watcher'] = watcher

        return self

    def _io(self, fd, w, revents):
        io = self._ios[fd]
        if revents & pyev.EV_READ:
            self._sandbox(io['cb'], 'Read', 0)
        if revents & pyev.EV_WRITE:
            self._sandbox(io['cb'], 'Write', 1)

    def _timer(self, cb, recurring, after):
        if recurring and not after:
            after = 0.0001

        tid = super(Pyjo_Reactor_EV, self)._timer(cb, 0, 0)
        self = weakref.proxy(self)

        def timer_cb(self, tid, watcher, revents):
            timer = self._timers[tid]
            if not recurring:
                self.remove(tid)
            self._sandbox(timer['cb'], 'Timer {0}'.format(tid))

        watcher = self._loop.timer(after, after,
                                   lambda watcher, revents:
                                   timer_cb(self, tid, watcher, revents))
        watcher.start()
        self._timers[tid]['watcher'] = watcher

        return tid


new = Pyjo_Reactor_EV.new
object = Pyjo_Reactor_EV  # @ReservedAssignment
