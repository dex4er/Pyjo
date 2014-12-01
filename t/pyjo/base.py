import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    from Pyjo.Base import *

    class A(Pyjo_Base):
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

    done_testing()
