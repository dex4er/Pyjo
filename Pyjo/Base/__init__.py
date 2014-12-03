"""
Pyjo.Base
"""

__all__ = ['Pyjo_Base']


class Omitted(object):
    pass


class Pyjo_Base(object):
    def set(self, *args, **kwargs):
        if args:
            for k, v in zip(args[::2], args[1::2]):
                setattr(self, k, v)
            if len(args) % 2:
                setattr(self, args[-1], None)
        elif kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        return self


def accessor(method):
    return property(method, method)


def not_implemented(method):
    def stub(*args, **kwargs):
        raise Error('Method "{0}" not implemented by subclass'.format(method.__name__))
    return stub


class Error(Exception):
    pass
