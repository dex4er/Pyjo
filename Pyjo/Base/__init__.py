# -*- coding: utf-8 -*-

"""
Pyjo.Base - Minimal base class
==============================
::

    import Pyjo.Base
    from Pyjo.Base import lazy

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


class Pyjo_Base(object):
    """::

        obj = SubClass.new()
        obj = SubClass.new(('name', 'value',))
        obj = SubClass.new(name='value')

    This base class provides a standard constructor for :mod:`Pyjo` objects. You can
    pass it either a list of pairs of tuples or a dict with attribute values.
    """
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
    def new(cls, *args, **kwargs):
        """
        Factory method for :mod:`Pyjo.Base` class.
        """
        return cls(*args, **kwargs)

    def set(self, *args, **kwargs):
        """::

            obj = obj.set(('name', 'value',))
            obj = obj.set(name='value')

        Sets each attribute from either a list of pairs of tuples or a dict.
        """
        for k, v in list(args) + list(kwargs.items()):
            setattr(self, k, v)
        return self

    def tap(self, _method, *args, **kwargs):
        """::

            obj = obj.tap(lambda obj: expression)
            obj = obj.tap(method)
            obj = obj.tap(method, *args, **kwargs)

        K combinator, tap into a method chain to perform operations on an object
        within the chain. The object will be the first argument passed to the callback. ::

            # Longer version
            obj = obj.tap(lambda obj: obj.method(args))

            # Inject side effects into a method chain
            obj.foo('A').tap(lambda obj: print(obj.foo)).set(foo='B')
        """
        if callable(_method):
            _method(self, *args, **kwargs)
        else:
            getattr(self, _method)(*args, **kwargs)
        return self


class lazy(object):
    """::

        import Pyjo.Base
        from Pyjo.Base import lazy

        class SubClass(Pyjo.Base.object):
            simple = lazy(42)
            complex = lazy(lambda self: [1, 2, 3])

        obj = SubClass.new()

        # False
        print('simple' in vars(obj))

        # 42
        print(obj.simple)

        # True
        print('simple' in vars(obj))

    Implementation of lazy attribute. The value is evaluated on first access
    to the attribute.
    """
    def __init__(self, default=None, name=None):
        self.default = default
        self.name = name

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        if callable(self.default):
            default = self.default(obj if obj is not None else objtype)
        else:
            default = self.default
        if self.name is None:
            return default
        setattr(obj, self.name, default)
        return getattr(obj, self.name)


new = Pyjo_Base.new
object = Pyjo_Base  # @ReservedAssignment
