# coding: utf-8

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

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

    isa_ok(string.to_str(), str, "string.to_str()")
    is_ok(string.to_str(), 'string', "string.to_str() == 'string'")

    is_ok(string2.to_str(), 'string', "string2.to_str() == 'string'")
    is_ok(other.to_str(), 'other', "other.to_str() == 'other'")

    isa_ok(str(string), str, "string.to_str()")
    is_ok(str(string), 'string', "str(string) == 'string'")

    ok(string == 'string', "string == 'string'")
    ok(string == string, "string == string")
    ok(string == string2, "string == string2")

    ok(not string != 'string', "not string != 'string'")
    ok(string != 'other', "string != 'other'")
    ok(string != other, "string != other")
    ok(not other != other, "not other != other")

    ok(not string > 'string', "not string > 'string'")
    ok(string > 'other', "string > 'other'")
    ok(not string > string, "not string > string")
    ok(string > other, "string > other")

    ok(string >= 'string', "string >= 'string'")
    ok(string >= 'other', "string >= 'other'")
    ok(string >= string, "string >= string")
    ok(string >= other, "string >= other")

    ok(not string < 'string', "not string < 'string'")
    ok(not string < 'other', "not string < 'other'")
    ok(not string < string, "not string < string")
    ok(not string < other, "string < other")

    ok(string <= 'string', "string <= 'string'")
    ok(not string <= 'other', "not string <= 'other'")
    ok(string <= string, "string <= string")
    ok(not string <= other, "not string <= other")

    ok(string, "string")
    ok(zero, "zero")
    ok(not empty, "not empty")

    ok(bool(string) is True, "bool(string) is True")
    ok(bool(zero) is True, "bool(zero) is True")
    ok(bool(empty) is False, "bool(empty) is False")

    if sys.version_info >= (3, 0):
        is_ok(bytes(string, 'ascii'), b'string', "bytes(string, 'ascii') == b'string'")
        is_ok(bytes(string, 'ascii'), bytes(string2, 'ascii'), "bytes(string, 'ascii') == bytes(string2, 'ascii')")
    else:
        skip('test for Python 3.x', 2)

    if sys.version_info < (3, 0):
        is_ok(unicode(string), u'string', "unicode(string) == u'string'")
        is_ok(unicode(string), unicode(string2), "unicode(string) == unicode(string2)")
    else:
        skip('test for Python 2.x', 2)

    is_ok(repr(string), "C('string')", "repr(string) == \"C('string')\"")

    done_testing()
