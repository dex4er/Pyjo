import os
import select
import socket

import Pyjo.EventEmmiter


class Error(Exception):
    pass


class object(Pyjo.EventEmmiter.object):

    def again(self):
        raise Error('Method "again" not implemented by subclass')

    def detect(self):
        return os.environ.get('PYJO_REACTOR', 'Pyjo.Reactor.Poll')

    def io(self):
        raise Error('Method "io" not implemented by subclass')

    # This may break at some point in the future, but is worth it for performance
    def is_readable(self, handle):
        p = select.poll()
        p.register(handle.fileno(), select.POLLIN | select.POLLPRI)
        return bool(p.poll(0))

    def is_running(self):
        raise Error('Method "is_running" not implemented by subclass')

    def next_tick(self, cb):
        self.timer(0, cb)

    def start(self):
        raise Error('Method "start" not implemented by subclass')

    def stop(self):
        raise Error('Method "stop" not implemented by subclass')

    def timer(self, after, cb):
        raise Error('Method "timer" not implemented by subclass')


def detect():
    return object().detect()
