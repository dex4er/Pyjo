"""
Pyjo.Reactor
"""

import select
import socket

from Pyjo.Base import *
from Pyjo.EventEmitter import *
from Pyjo.Util import getenv, not_implemented


__all__ = ['Pyjo_Reactor']


class Error(Exception):
    pass


class Pyjo_Reactor(Pyjo_EventEmitter):

    @not_implemented
    def again(self):
        pass

    @classmethod
    def detect(self):
        return getenv('PYJO_REACTOR', 'Pyjo.Reactor.Poll')

    @not_implemented
    def io(self):
        pass

    # This may break at some point in the future, but is worth it for performance
    def is_readable(self, handle):
        p = select.poll()
        p.register(handle.fileno(), select.POLLIN | select.POLLPRI)
        return bool(p.poll(0))

    @not_implemented
    def is_running(self):
        pass

    def next_tick(self, cb):
        self.timer(0, cb)

    @not_implemented
    def one_tick(self):
        pass

    @not_implemented
    def recurring(self, after, cb):
        pass

    @not_implemented
    def remove(self, remove):
        pass

    @not_implemented
    def reset(self):
        pass

    @not_implemented
    def start(self):
        pass

    @not_implemented
    def stop(self):
        pass

    @not_implemented
    def timer(self, after, cb):
        pass

    @not_implemented
    def watch(self, handle, read, write):
        pass
