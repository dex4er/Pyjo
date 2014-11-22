"""
Pyjo.Reactor
"""

import select
import socket

import Pyjo.EventEmitter

from Pyjo.Base import moduleobject
from Pyjo.Util import getenv


class Error(Exception):
    pass


def not_implemented(_method):
    def stub(*args, **kwargs):
        raise Error('Method "{0}" not implemented by subclass'.format(_method.__name__))
    return stub


@moduleobject
class Pyjo_Reactor(Pyjo.EventEmitter.object):

    @not_implemented
    def again(self):
        pass

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


def detect():
    return object().detect()
