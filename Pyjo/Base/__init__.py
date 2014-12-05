"""
Pyjo.Base
"""


from Pyjo.Util import lazy


class Pyjo_Base(object):
    def __new__(cls, *args, **kwargs):
        obj = super(Pyjo_Base, cls).__new__(cls)
        for name in dir(obj):
            attr = getattr(cls, name)
            if attr.__class__.__name__ == 'lazy':
                setattr(cls, name, lazy(attr.default, name))
        return obj

    def __init__(self, *args, **kwargs):
        self.set(*args, **kwargs)

    @classmethod
    def attr(cls, attrs, default=None):
        if not isinstance(attrs, (list, tuple)):
            attrs = [attrs]

        for attr in attrs:
            setattr(cls, attr, lazy(default, attr))

        return cls

    def set(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self


def new(*args, **kwargs):
    return Pyjo_Base(*args, **kwargs)


object = Pyjo_Base  # @ReservedAssignment
