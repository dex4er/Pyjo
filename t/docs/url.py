# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.URL

    # __init __
    # Parse
    url = Pyjo.URL.new('http://sri:foobar@example.com:3000/foo/bar?foo=bar#23')
    is_ok(url.scheme, 'http', "url.scheme")
    is_ok(url.userinfo, 'sri:foobar', "url.userinfo")
    is_ok(url.host, 'example.com', "url.host")
    is_ok(url.port, 3000, "url.port")
    is_ok(url.path, '/foo/bar', "url.path")
    is_ok(url.query.to_dict(), {'foo': 'bar'}, "url.query.to_dict()")
    is_ok(url.fragment, '23', "url.fragment")

    # Build
    url = Pyjo.URL.new()
    url.scheme = 'http'
    url.userinfo = 'sri:foobar'
    url.host = 'example.com'
    url.port = 3000
    url.path = '/foo/bar'
    url.query.param('foo', 'bar')
    url.fragment = '23'
    is_ok(url.to_str(), 'http://sri:foobar@example.com:3000/foo/bar?foo=bar#23', "url")

    
    done_testing()
