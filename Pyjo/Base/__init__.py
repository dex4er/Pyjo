"""
Pyjo.Base
"""


from Pyjo.Util import lazy


class Pyjo_Base(object):
    def __init__(self, *args, **kwargs):
        self.set(*args, **kwargs)

    @classmethod
    def attr(cls, attrs, default=None):
        if not isinstance(attrs, (list, tuple)):
            attrs = [attrs]

        for attr in attrs:
            setattr(cls, attr, lazy(attr, default))

        return cls

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
    return Pyjo_Base(*args, **kwargs)


object = Pyjo_Base  # @ReservedAssignment
