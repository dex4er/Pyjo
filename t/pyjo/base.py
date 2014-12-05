import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Base

    class A(Pyjo.Base.object):
        pass

    obj = A()
    isa_ok(obj, A, 'obj')

    obj.set(a=1, b=2)
    is_ok(obj.a, 1, 'obj.a is 1')
    is_ok(obj.b, 2, 'obj.b is 2')

    obj.set('c', 3, 'd', 4, 'e')
    is_ok(obj.c, 3, 'obj.c is 3')
    is_ok(obj.d, 4, 'obj.d is 4')
    none_ok(obj.e, 'obj.e')

    obj = A(g=1, h=2)
    isa_ok(obj, A, 'obj')
    is_ok(obj.g, 1, 'obj.g is 1')
    is_ok(obj.h, 2, 'obj.h is 2')

    obj = A('i', 3, 'j', 4)
    isa_ok(obj, A, 'obj')
    is_ok(obj.i, 3, 'obj.i is 3')
    is_ok(obj.j, 4, 'obj.j is 4')


    done_testing()
