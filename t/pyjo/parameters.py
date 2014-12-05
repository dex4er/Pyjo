# coding: utf-8

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Parameters

    # Basic functionality
    params = Pyjo.Parameters.new('foo=b%3Bar&baz=23')
    params2 = Pyjo.Parameters.new('x', 1, 'y', 2)
    params3 = Pyjo.Parameters.new(a=1, b=2, c=3, d=4)
    is_ok(params.to_string(), 'foo=b%3Bar&baz=23', 'right format')
    is_ok(params2.to_string(), 'x=1&y=2', 'right format')
    is_ok(params3.to_string(), 'a=1&b=2&c=3&d=4', 'right format')
    is_ok(params.to_string(), 'foo=b%3Bar&baz=23', 'right format')
    # is_deeply_ok(params.params(), ['foo', 'b;ar', 'baz', 23], 'right structure')

    done_testing()
