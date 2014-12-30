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

    # Parse
    url = Pyjo.URL.new('http://sri:foobar@example.com:3000/foo/bar?foo=bar#23')
    is_ok(url.scheme, 'http', "url.scheme")
    is_ok(url.userinfo, 'sri:foobar', "url.userinfo")
    is_ok(url.host, 'example.com', "url.host")
    is_ok(url.port, 3000, "url.port")
    is_ok(url.path, '/foo/bar', "url.path")
    is_ok(url.query, 'foo=bar', "url.query.to_dict()")
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
    is_ok(url, 'http://sri:foobar@example.com:3000/foo/bar?foo=bar#23', "url")

    # __init __
    url = Pyjo.URL.new()
    is_ok(url, '', "url")
    url = Pyjo.URL.new('http://127.0.0.1:3000/foo?f=b&baz=2#foo')
    is_ok(url, 'http://127.0.0.1:3000/foo?f=b&baz=2#foo', "url")

    # Attributes
    url = Pyjo.URL.new()

    base = url.base
    is_ok(base, '', "base")
    url.base = Pyjo.URL.new()
    is_ok(url.base, '', "url.base")

    fragment = url.fragment
    is_ok(fragment, None, "fragment")
    url.fragment = u'♥pyjo♥'
    is_ok(url.fragment, u'♥pyjo♥', "url.fragment")

    host = url.host
    is_ok(host, None, "host")
    url.host = '127.0.0.1'
    is_ok(url.host, '127.0.0.1', "url.host")

    port = url.port
    is_ok(port, None, "port")
    url.port = 8080
    is_ok(url.port, 8080, "url.port")

    scheme = url.scheme
    is_ok(scheme, None, "scheme")
    url.scheme = 'http'
    is_ok(url.scheme, 'http', "url.scheme")

    userinfo = url.userinfo
    is_ok(userinfo, None, "userinfo")
    url.userinfo = u'root:♥'
    is_ok(url.userinfo, u'root:♥', "url.userinfo")

    # authority
    url = Pyjo.URL.new()
    authority = url.authority
    is_ok(authority, None, "authority")
    url.authority = 'root:%E2%99%A5@localhost:8080'
    is_ok(url.authority, 'root:%E2%99%A5@localhost:8080', "url.authority")

    authority = Pyjo.URL.new(u'http://root:♥@☃.net:8080/test').authority
    is_ok(authority, "root:%E2%99%A5@xn--n3h.net:8080", "authority")

    authority = Pyjo.URL.new('http://root@example.com/test').authority
    is_ok(authority, "root@example.com", "authority")

    # clone
    url = Pyjo.URL.new('http://sri:foobar@example.com:3000/foo/bar?foo=bar#23')
    url2 = url.clone()
    is_ok(url2, 'http://sri:foobar@example.com:3000/foo/bar?foo=bar#23', "url2")

    done_testing()
