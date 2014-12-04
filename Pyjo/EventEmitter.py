"""
Pyjo.EventEmitter
"""

import weakref

from Pyjo.Base import *
from Pyjo.Util import getenv, warn


__all__ = ['Pyjo_EventEmitter']


DEBUG = getenv('PYJO_EVENTEMITTER_DEBUG', 0)


class Error(Exception):
    pass


class Pyjo_EventEmitter(Pyjo_Base):
    def __init__(self):
        self._events = {}

    def catch(self, *args):
        self.on('error', *args)
        return self

    def emit(self, name, *args, **kwargs):
        if name in self._events:
            s = self._events[name]
            if DEBUG:
                warn("-- Emit {0} in {1} ({2})".format(name, self, len(s)))
            for cb in s:
                cb(self, *args)
        else:
            if DEBUG:
                warn("-- Emit {0} in {1} (0)".format(name, self))
            if name == 'error':
                raise Error(*args)
        return self

    def has_subscribers(self, name):
        return name in self._events

    def on(self, name, cb):
        if name in self._events:
            self._events[name].append(cb)
        else:
            self._events[name] = [cb]
        return cb

    def once(self, name, cb):
        self = weakref.proxy(self)

        def wrapper_cb(self, name, cb, wrapper_lambda, *args):
            self.unsubscribe(name, wrapper_lambda)
            cb(*args)

        wrapper_lambda = lambda *args: wrapper_cb(self, name, cb, wrapper_lambda, *args)
        self.on(name, wrapper_lambda)

        # TODO weakref.proxy(wrapper_lambda)

        return wrapper_lambda

    def subscribers(self, name):
        return self._events[name]

    def unsubscribe(self, name, cb=None):
        # One
        if cb:
            self._events[name] = [a for a in self._events[name] if a != cb]
            if not len(self._events[name]):
                del self._events[name]

        # All
        else:
            del self._events[name]

        return self


def new(*args, **kwargs):
    return Pyjo_EventEmitter(*args, **kwargs)
