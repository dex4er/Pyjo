# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Parameters

    # Parse
    params = Pyjo.Parameters.new('foo=bar&baz=23')
    is_ok(params.param('baz'), '23', "params.param('baz')")

    # Build
    params = Pyjo.Parameters.new('foo', 'bar', 'baz', '23')
    params.append(i='♥ Pyjo')
    is_ok(params.to_string(), 'foo=bar&baz=23&i=%E2%99%A5+Pyjo', 'params')

    done_testing()
