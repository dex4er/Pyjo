"""
Pyjo.Reactor
"""

import os
import select
import socket

import Pyjo.Base
import Pyjo.EventEmitter

from Pyjo.Util import getenv, not_implemented


class Error(Exception):
    pass


class Pyjo_Reactor(Pyjo.EventEmitter.object):

    @not_implemented
    def again(self):
        pass

    @classmethod
    def detect(self):
        if os.name == "nt":
            default = 'Pyjo.Reactor.Select'
        else:
            default = 'Pyjo.Reactor.Poll'
        return getenv('PYJO_REACTOR', default)

    @not_implemented
    def io(self, cb, handle):
        pass

    @not_implemented
    def is_readable(self, handle):
        pass

    @not_implemented
    def is_running(self):
        pass

    def next_tick(self, cb):
        self.timer(cb, 0)

    @not_implemented
    def one_tick(self):
        pass

    @not_implemented
    def recurring(self, cb, after):
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
    def timer(self, cb, after):
        pass

    @not_implemented
    def watch(self, handle, read, write):
        pass


detect = Pyjo_Reactor.detect

new = Pyjo_Reactor.new
object = Pyjo_Reactor  # @ReservedAssignment
