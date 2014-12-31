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

    # host_port
    url = Pyjo.URL.new()
    host_port = url.host_port
    is_ok(host_port, None, "host_port")

    host_port = Pyjo.URL.new(u'http://☃.net:8080/test').host_port
    is_ok(host_port, 'xn--n3h.net:8080', "host_port")

    host_port = Pyjo.URL.new('http://example.com/test').host_port
    is_ok(host_port, 'example.com', "host_port")

    # ihost
    url = Pyjo.URL.new()
    ihost = url.ihost
    is_ok(ihost, None, "ihost")
    url.ihost = 'xn--bcher-kva.ch'
    is_ok(url.ihost, 'xn--bcher-kva.ch', "url.ihost")

    ihost = Pyjo.URL.new(u'http://☃.net').ihost
    is_ok(ihost, "xn--n3h.net", "ihost")

    ihost = Pyjo.URL.new('http://example.com').ihost
    is_ok(ihost, "example.com", "ihost")

    # is_abs
    url = Pyjo.URL.new()
    boolean = url.is_abs()
    is_ok(boolean, False, "boolean")

    boolean = Pyjo.URL.new('http://example.com').is_abs()
    is_ok(boolean, True, "boolean")
    boolean = Pyjo.URL.new('http://example.com/test/index.html').is_abs()
    is_ok(boolean, True, "boolean")

    boolean = Pyjo.URL.new('test/index.html').is_abs()
    is_ok(boolean, False, "boolean")
    boolean = Pyjo.URL.new('/test/index.html').is_abs()
    is_ok(boolean, False, "boolean")
    boolean = Pyjo.URL.new('//example.com/test/index.html').is_abs()
    is_ok(boolean, False, "boolean")

    # parse
    url = Pyjo.URL.new()
    url = url.parse('http://127.0.0.1:3000/foo/bar?fo=o&baz=23#foo')
    is_ok(url, 'http://127.0.0.1:3000/foo/bar?fo=o&baz=23#foo', "url")

    url = Pyjo.URL.new()
    path = url.parse('/test/123?foo=bar').path
    is_ok(path, '/test/123', "path")

    url = Pyjo.URL.new()
    host = url.parse('http://example.com/test/123?foo=bar').host
    is_ok(host, 'example.com', "host")

    url = Pyjo.URL.new()
    path = url.parse('mailto:sri@example.com').path
    is_ok(path, "sri@example.com", "path")

    # path
    url = Pyjo.URL.new()
    path = url.path
    is_ok(url, '', "url")
    url = Pyjo.URL.new()
    url.path = '/foo/bar'
    is_ok(url, '/foo/bar', "url")
    url = Pyjo.URL.new()
    url.path = 'foo/bar'
    is_ok(url, 'foo/bar', "url")
    url = Pyjo.URL.new()
    url.path = Pyjo.Path.new()
    is_ok(url, '', "url")

    part = Pyjo.URL.new('http://example.com/perldoc/Mojo').path.parts[0]
    is_ok(part, "perldoc", "part")

    url = Pyjo.URL.new('http://example.com/perldoc/Mojo').set(path='/DOM/HTML')
    is_ok(url, "http://example.com/DOM/HTML", "url")

    url = Pyjo.URL.new('http://example.com/perldoc/Mojo').set(path='DOM/HTML')
    is_ok(url, "http://example.com/perldoc/DOM/HTML", "url")

    url = Pyjo.URL.new('http://example.com/perldoc/Mojo/').set(path='DOM/HTML')
    is_ok(url, "http://example.com/perldoc/Mojo/DOM/HTML", "url")

    # path_query
    url = Pyjo.URL.new()
    path_query = url.path_query
    is_ok(path_query, "", "path_query")

    path_query = Pyjo.URL.new('http://example.com/test?a=1&b=2').path_query
    is_ok(path_query, "/test?a=1&b=2", "path_query")

    path_query = Pyjo.URL.new('http://example.com/').path_query
    is_ok(path_query, "/", "path_query")

    # protocol
    url = Pyjo.URL.new()
    proto = url.protocol
    is_ok(proto, "", "proto")

    proto = Pyjo.URL.new('HtTp://example.com').protocol
    is_ok(proto, "http", "proto")

    done_testing()
