"""
Pyjo.EventEmitter
"""

import weakref

import Pyjo.Base

from Pyjo.Util import getenv, lazy, warn


DEBUG = getenv('PYJO_EVENTEMITTER_DEBUG', 0)


class Error(Exception):
    pass


class Pyjo_EventEmitter(Pyjo.Base.object):

    _events = lazy(lambda: {})

    def catch(self, cb):
        self.on(cb, 'error')
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

    def on(self, cb, name=None):
        if name is None:
            name = cb.__name__

        if name in self._events:
            self._events[name].append(cb)
        else:
            self._events[name] = [cb]
        return cb

    def once(self, cb, name=None):
        if name is None:
            name = cb.__name__

        self = weakref.proxy(self)

        def wrap_cb(self, cb, name, wrap_lambda, *args):
            self.unsubscribe(name, wrap_lambda)
            cb(*args)

        wrap_lambda = lambda *args: wrap_cb(self, cb, name, wrap_lambda, *args)
        self.on(wrap_lambda, name)

        # TODO weakref.proxy(wrap_lambda)

        return wrap_lambda

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


new = Pyjo_EventEmitter.new
object = Pyjo_EventEmitter  # @ReservedAssignment
