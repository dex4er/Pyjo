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
    params = Pyjo.Parameters.new('foo', 'bar', 'baz', 23)
    params.append(i='♥ Pyjo')
    is_ok(params.to_str(), 'foo=bar&baz=23&i=%E2%99%A5+Pyjo', 'params')

    pass_ok('__init__')
    params = Pyjo.Parameters.new()
    is_ok(params.to_str(), '', 'params')

    params = Pyjo.Parameters.new('foo=b%3Bar&baz=23')
    is_ok(params.to_str(), 'foo=b%3Bar&baz=23', 'params')

    params = Pyjo.Parameters.new(foo='b&ar')
    is_ok(params.to_str(), 'foo=b%26ar', 'params')

    params = Pyjo.Parameters.new(foo=['ba&r', 'baz'])
    is_ok(params.to_str(), 'foo=ba%26r&foo=baz', 'params')

    params = Pyjo.Parameters.new(foo=['bar', 'baz'], bar=23)
    is_ok(params.to_str(), 'bar=23&foo=bar&foo=baz', 'params')

    pass_ok('append')
    params = Pyjo.Parameters.new('foo=bar').append(foo='baz')
    is_ok(params.to_str(), 'foo=bar&foo=baz', 'params')

    params = Pyjo.Parameters.new('foo=bar').append(foo=['baz', 'yada'])
    is_ok(params.to_str(), 'foo=bar&foo=baz&foo=yada', 'params')

    params = Pyjo.Parameters.new('foo=bar').append('foo', ['baz', 'yada'], 'bar', 23)
    is_ok(params.to_str(), 'foo=bar&foo=baz&foo=yada&bar=23', 'params')

    pass_ok('clone')
    params = Pyjo.Parameters.new('foo=b%3Bar&baz=23')
    params2 = params.clone()
    is_ok(params2.to_str(), 'foo=b%3Bar&baz=23', 'params2')

    pass_ok('every_param')
    params = Pyjo.Parameters.new('bar=23&foo=bar&foo=baz')
    values = params.every_param('foo')
    is_deeply_ok(values, ['bar', 'baz'], "params.every_param('foo')")

    # Get first value
    value = params.every_param('foo')[0]
    is_ok(value, 'bar', "params.every_param('foo')[0]")

    pass_ok('param')
    params = Pyjo.Parameters.new('foo=bar&baz=23')
    names = params.param()
    is_deeply_ok(names, ['baz', 'foo'], "params.param()")
    value = params.param('foo')
    is_ok(value, 'bar', "params.param('foo')")
    foo, baz = params.param(['foo', 'baz'])
    is_ok(foo, 'bar', "params.param(['foo', 'baz'])[0]")
    is_ok(baz, '23', "params.param(['foo', 'baz'])[1]")
    params = params.param('foo', 'ba&r')
    is_ok(params.to_str(), 'baz=23&foo=ba%26r', "params.param('foo', 'ba&r')")
    params = params.param('foo', ['ba;r', 'baz'])
    is_ok(params.to_str(), 'baz=23&foo=ba%3Br&foo=baz', "params.param('foo', ['ba;r', 'baz'])")

    pass_ok('params')
    params = Pyjo.Parameters.new('foo=bar&baz=23')
    array = params.params
    is_deeply_ok(array, ['foo', 'bar', 'baz', '23'], "params.params")
    params.params = ['foo', 'b&ar', 'baz', 23]
    is_ok(params.to_str(), 'foo=b%26ar&baz=23', "params")

    pass_ok('parse')
    params = Pyjo.Parameters.new()
    params = params.parse('foo=b%3Bar&baz=23')
    is_deeply_ok(params.params, ['foo', 'b;ar', 'baz', '23'], "params.parse('foo=b%3Bar&baz=23')")

    pass_ok('remove')
    params = Pyjo.Parameters.new('foo=bar&foo=baz&bar=yada').remove('foo')
    is_ok(params.to_str(), 'bar=yada', "params.remove('foo')")

    pass_ok('to_dict')
    d = Pyjo.Parameters.new('foo=bar&foo=baz').to_dict()
    is_deeply_ok(d, {'foo': ['bar', 'baz']}, "params.to_dict()")

    done_testing()
