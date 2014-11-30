"""
Pyjo.Reactor.EV
"""

import pyev
import weakref

from Pyjo.Reactor.Poll import *


__all__ = ['Pyjo_Reactor_EV']


class Pyjo_Reactor_EV(Pyjo_Reactor_Poll):
    def __init__(self):
        super(Pyjo_Reactor_EV, self).__init__()

        self._loop = pyev.default_loop()

    def again(self, tid):
        self._timers[tid]['watcher'].reset()

    def is_running(self):
        return self._loop.depth

    def one_tick(self):
        self._loop.start(pyev.EVRUN_ONCE)

    def recurring(self, after, cb):
        return self._timer(True, after, cb)

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

    def timer(self, *args, **kwargs):
        return self._timer(False, *args, **kwargs)

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
                                        lambda watcher, revents: \
                                        self._io(fd, watcher, revents))
                watcher.start()
                io['watcher'] = watcher

        return self

    def _poll(self):
        return

    def _io(self, fd, w, revents):
        io = self._ios[fd]
        if revents & pyev.EV_READ:
            self._sandbox('Read', io['cb'], 0)
        if revents & pyev.EV_WRITE:
            self._sandbox('Write', io['cb'], 1)

    def _timer(self, recurring, after, cb):
        if recurring and not after:
            after = 0.0001

        tid = super(Pyjo_Reactor_EV, self)._timer(0, 0, cb)
        self = weakref.proxy(self)

        def timer_cb(self, tid, watcher, revents):
            timer = self._timers[tid]
            if not recurring:
                self.remove(tid)
            self._sandbox('Timer {0}'.format(tid), timer['cb'])

        watcher = self._loop.timer(after, after,
                                   lambda watcher, revents: \
                                   timer_cb(self, tid, watcher, revents))
        watcher.start()
        self._timers[tid]['watcher'] = watcher

        return tid
