# -*- coding: utf-8 -*-

"""
Pyjo.Base - Minimal base class
==============================
::

    import Pyjo.Base
    from Pyjo.Util import lazy

    class Cat(Pyjo.Base.object):
        name = 'Nyan'
        birds = 2
        mice = 2

    class Tiger(Cat):
        friends = lazy(lambda self: Cat())
        stripes = 42

    mew = Cat.new(name='Longcat')
    print(mew.mice)
    print(mew.set(mice=3, birds=4).mice)

    rawr = Tiger.new(stripes=23, mice=0)
    print(rawr.tap(lambda self: self.friend.set(name='Tacgnol').mice))

:mod:`Pyjo.Base` is a simple base class for :mod:`Pyjo` projects.
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

    def __init__(self, **kwargs):
        self.set(**kwargs)

    @classmethod
    def attr(cls, attrs, default=None):
        if not isinstance(attrs, (list, tuple)):
            attrs = [attrs]

        for attr in attrs:
            setattr(cls, attr, lazy(default, attr))

        return cls

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def set(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self


new = Pyjo_Base.new
object = Pyjo_Base  # @ReservedAssignment
