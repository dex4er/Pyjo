"""
Pyjo.Base
"""


class _object(object):
    def __init__(self, *args, **kwargs):
        self.set(*args, **kwargs)


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


def new(*args, **kwargs):
    return _object(*args, **kwargs)


object = _object  # @ReservedAssignment
