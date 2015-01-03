import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Base

    from Pyjo.Util import lazy

    class A(Pyjo.Base.object):
        pass

    obj = A()
    isa_ok(obj, A, 'obj')

    obj.set(a=1, b=2)
    is_ok(obj.a, 1, 'obj.a')
    is_ok(obj.b, 2, 'obj.b')

    obj = A(c=1, d=2)
    isa_ok(obj, A, 'obj')
    is_ok(obj.c, 1, 'obj.c')
    is_ok(obj.d, 2, 'obj.d')

    class B(Pyjo.Base.object):
        a = 1
        b = 2
        c = lazy(3)
        d = 45
        e = 45

    obj = B()

    isa_ok(obj, B, 'obj')

    is_ok(obj.a, 1, 'obj.a')
    is_ok(obj.b, 2, 'obj.b')
    is_ok(obj.c, 3, 'obj.c')
    is_ok(obj.d, 45, 'obj.d')
    is_ok(obj.e, 45, 'obj.e')

    class C(Pyjo.Base.object):
        a = 1

    obj1 = C()

    isa_ok(obj1, C, 'obj1')

    obj2 = C()

    isa_ok(obj2, C, 'obj2')

    is_ok(obj1.a, 1, 'obj1.a')

    obj1.a = 11

    is_ok(obj1.a, 11, 'obj1.a')
    is_ok(obj2.a, 1, 'obj2.a')

    obj3 = C()

    isa_ok(obj3, C, 'obj3')

    is_ok(obj3.a, 1, 'obj3.a')
    is_ok(obj2.a, 1, 'obj2.a')
    is_ok(obj1.a, 11, 'obj1.a')

    obj2.a = 2

    is_ok(obj3.a, 1, 'obj3.a')
    is_ok(obj2.a, 2, 'obj2.a')
    is_ok(obj1.a, 11, 'obj1.a')

    obj4 = C(a=4)

    is_ok(obj4.a, 4, 'obj4.a')
    is_ok(obj3.a, 1, 'obj3.a')
    is_ok(obj2.a, 2, 'obj2.a')
    is_ok(obj1.a, 11, 'obj1.a')

    obj5 = C()

    isa_ok(obj5, C, 'obj5')

    is_ok(obj5.a, 1, 'obj5.a')

    class D(Pyjo.Base.object):
        a = None
        b = 2
        c = lazy(3)
        d = lazy(lambda self: 4)

    obj = D()

    isa_ok(obj, D, 'obj')
    none_ok(obj.a, 'obj.a')
    is_ok(obj.b, 2, 'obj.b')
    is_ok(obj.c, 3, 'obj.c')
    is_ok(obj.d, 4, 'obj.d')

    done_testing()
