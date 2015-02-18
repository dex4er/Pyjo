# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Base
    from Pyjo.Base import lazy

    class Cat(Pyjo.Base.object):
        name = 'Nyan'
        birds = 2
        mice = 2

    class Tiger(Cat):
        friend = lazy(lambda self: Cat())
        stripes = 42

    mew = Cat.new(name='Longcat')
    is_ok(mew.mice, 2, "mew.mice")
    is_ok(mew.set(mice=3, birds=4).mice, 3, "mew.set(...).mice")

    rawr = Tiger.new(stripes=23, mice=0)
    is_ok(rawr.tap(lambda rawr: rawr.friend.set(name='Tacgnol')).mice, 0, "rawr.tap(...).mice")

    class SubClass(Pyjo.Base.object):
        name = None

    # new
    obj = SubClass.new()
    isa_ok(obj, SubClass, "obj")
    none_ok(obj.name, "obj.name")

    obj = SubClass.new(('name', 'value'),)
    is_ok(obj.name, 'value', "obj.name")
    obj = SubClass.new(name='value')
    is_ok(obj.name, 'value', "obj.name")

    # set
    obj = SubClass.new()
    obj = obj.set(('name', 'value'),)
    isa_ok(obj, SubClass, "obj")
    is_ok(obj.name, 'value', "obj.name")

    obj = SubClass.new()
    obj = obj.set(name='value')
    isa_ok(obj, SubClass, "obj")
    is_ok(obj.name, 'value', "obj.name")

    # tap
    obj = SubClass.new()
    obj = obj.tap(lambda obj: obj.set(name='value'))
    isa_ok(obj, SubClass, "obj")
    is_ok(obj.name, 'value', "obj.name")

    obj = SubClass.new()
    obj = obj.tap('set', ('name', 'value'),)
    isa_ok(obj, SubClass, "obj")
    is_ok(obj.name, 'value', "obj.name")

    obj = SubClass.new()
    obj = obj.tap('set', name='value')
    isa_ok(obj, SubClass, "obj")
    is_ok(obj.name, 'value', "obj.name")

    # lazy
    class SubClass(Pyjo.Base.object):
        simple = lazy(42)
        complex = lazy(lambda self: [1, 2, 3])

    obj = SubClass.new()
    isa_ok(obj, SubClass, "obj")

    ok('simple' not in vars(obj), "'simple' in vars(obj)")
    is_ok(obj.simple, 42, "obj.simple")
    ok('simple' in vars(obj), "'simple' in vars(obj)")

    done_testing()
