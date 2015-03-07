# coding: utf-8

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import platform
    import sys

    import Pyjo.Base
    import Pyjo.Mixin.String

    class C(Pyjo.Base.object, Pyjo.Mixin.String.object):
        value = None

        def to_str(self):
            return self.value

    string = C(value='string')
    string2 = C(value='string')
    other = C(value='other')
    zero = C(value='0')
    empty = C(value='')

    isa_ok(string, C, 'string')
    isa_ok(string2, C, 'string2')
    isa_ok(other, C, 'other')
    isa_ok(zero, C, 'zero')
    isa_ok(empty, C, 'empty')

    # to_str
    isa_ok(string.to_str(), str, "string.to_str()")
    is_ok(string.to_str(), 'string', "string.to_str() == 'string'")

    is_ok(string2.to_str(), 'string', "string2.to_str() == 'string'")
    is_ok(other.to_str(), 'other', "other.to_str() == 'other'")

    # __bool__
    if sys.version_info >= (3, 0):
        ok(bool(string) is True, "bool(string) is True")
        ok(bool(zero) is True, "bool(zero) is True")
        ok(bool(empty) is False, "bool(empty) is False")
    else:
        skip('test for Python 3.x', 3)

    # __bytes__
    if sys.version_info >= (3, 0) and sys.version_info <= (3, 4):
        is_ok(bytes(string, 'ascii'), b'string', "bytes(string, 'ascii') == b'string'")
        is_ok(bytes(string, 'ascii'), bytes(string2, 'ascii'), "bytes(string, 'ascii') == bytes(string2, 'ascii')")
    else:
        skip('test for Python 3.[0-4]', 2)

    # __complex__
    is_ok(repr(complex(zero)), '0j', "complex(zero)")

    # __eq__
    ok(string == 'string', "string == 'string'")
    ok(string == string, "string == string")
    ok(string == string2, "string == string2")

    # __float__
    is_ok(repr(float(zero)), '0.0', "float(zero)")

    # __ge__
    ok(string >= 'string', "string >= 'string'")
    ok(string >= 'other', "string >= 'other'")
    ok(string >= string, "string >= string")
    ok(string >= other, "string >= other")

    # __gt__
    ok(not string > 'string', "not string > 'string'")
    ok(string > 'other', "string > 'other'")
    ok(not string > string, "not string > string")
    ok(string > other, "string > other")

    # __hash__
    ok(isinstance(hash(string), int), "hash(string)")

    # __hex__
    if sys.version_info < (3, 0):
        is_ok(repr(hex(zero)), "'0x0'", "hex(zero)")
    else:
        skip('test for Python 2.x')

    # __int__
    if platform.python_implementation() != 'PyPy' or sys.version_info < (3, 0):
        is_ok(repr(int(zero)), '0', "int(zero)")
    else:
        skip('PyPy3 error')

    # __le__
    ok(string <= 'string', "string <= 'string'")
    ok(not string <= 'other', "not string <= 'other'")
    ok(string <= string, "string <= string")
    ok(not string <= other, "not string <= other")

    # __long__
    if sys.version_info < (3, 0):
        is_ok(repr(long(zero)), '0L', "long(zero)")
    else:
        skip('test for Python 2.x')

    # __lt__
    ok(not string < 'string', "not string < 'string'")
    ok(not string < 'other', "not string < 'other'")
    ok(not string < string, "not string < string")
    ok(not string < other, "string < other")

    # __ne__
    ok(not string != 'string', "not string != 'string'")
    ok(string != 'other', "string != 'other'")
    ok(string != other, "string != other")
    ok(not other != other, "not other != other")

    # __nonzero__
    if sys.version_info < (3, 0):
        ok(bool(string) is True, "bool(string) is True")
        ok(bool(zero) is True, "bool(zero) is True")
        ok(bool(empty) is False, "bool(empty) is False")
    else:
        skip('test for Python 2.x', 3)

    # __oct__
    if sys.version_info < (3, 0):
        is_ok(repr(oct(zero)), "'0'", "oct(zero)")
    else:
        skip('test for Python 2.x')

    # __repr__
    is_ok(repr(string), "C('string')", "repr(string) == \"C('string')\"")

    # __str__
    isa_ok(str(string), str, "string.to_str()")
    is_ok(str(string), 'string', "str(string) == 'string'")

    # __unicode__
    if sys.version_info < (3, 0):
        is_ok(unicode(string), u'string', "unicode(string) == u'string'")
        is_ok(unicode(string), unicode(string2), "unicode(string) == unicode(string2)")
    else:
        skip('test for Python 2.x', 2)

    done_testing()
