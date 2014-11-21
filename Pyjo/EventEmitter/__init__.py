"""
Pyjo.EventEmitter
"""

import Pyjo.Base

from Pyjo.Base import moduleobject
from Pyjo.Util import getenv, warn


DEBUG = getenv('PYJO_EVENTEMITTER_DEBUG', 0)


class Error(Exception):
    pass


@moduleobject
class _(Pyjo.Base.object):
    _events = {}

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

    def on(self, name, cb):
        if name in self._events:
            self._events[name].append(cb)
        else:
            self._events[name] = [cb]
        return cb

    def once(self, name, cb):
        # TODO weaken self
        def wrapper(*args):
            self.unsubscribe(name, wrapper)
            cb(*args)
        self.on(name, wrapper)
        # weaken wrapper

        return wrapper

    def subscribers(self, name):
        return self._events[name]

    def unsubscribe(self, name, cb=None):
        # One
        if cb:
            self._events[name] = filter(lambda e: e != cb, self._events[name])
            if not len(self._events[name]):
                del self._events[name]

        # All
        else:
            del self._events[name]

        return self
