# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Path

    # __init __
    path = Pyjo.Path.new()
    is_ok(path.to_str(), '', "path")
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    is_ok(path.to_str(), '/foo%2Fbar%3B/baz.html', "path")

    # charset
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    charset = path.charset
    is_ok(charset, 'utf-8', "charset")
    path.charset = 'utf-8'
    charset = path.charset
    is_ok(charset, 'utf-8', "charset")

    # __iter__
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    l = [v for v in path]
    is_deeply_ok(l, [u'foo', u'bar;', u'baz.html'], "[v for v in path]")

    # __bool__
    ok(Pyjo.Path.new(), "Pyjo.Path.new()")

    # canonicalize
    path = Pyjo.Path.new('/foo/./bar/../baz').canonicalize()
    is_ok(path.to_str(), "/foo/baz", "path")

    path = Pyjo.Path.new('/foo/../bar/../../baz').canonicalize()
    is_ok(path.to_str(), "/../baz", "path")

    # clone
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    path2 = path.clone()
    is_ok(path2.to_str(), '/foo%2Fbar%3B/baz.html', 'path2')
    isnt_ok(id(path), id(path2), 'path')

    # leading_slash
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    leading_slash = path.leading_slash
    is_ok(leading_slash, True, "leading_slash")
    path.leading_slash = False
    leading_slash = path.leading_slash
    is_ok(leading_slash, False, "leading_slash")

    # parse
    path = Pyjo.Path.new()
    path = path.parse('/foo%2Fbar%3B/baz.html')
    is_deeply_ok(path.parts, [u'foo', u'bar;', u'baz.html'], "path.parts")

    # paths
    path = Pyjo.Path.new()
    path.parts = ['foo', 'bar', 'baz']
    is_ok(path.to_str(), 'foo/bar/baz', 'path')

    path.parts.append('foo/bar')
    is_ok(path.to_str(), 'foo/bar/baz/foo%2Fbar', 'path')

    # to_abs_str
    path = Pyjo.Path.new('/i/%E2%99%A5/mojolicious').to_abs_str()
    is_ok(path, "/i/%E2%99%A5/mojolicious", "path")

    path = Pyjo.Path.new('i/%E2%99%A5/mojolicious').to_abs_str()
    is_ok(path, "/i/%E2%99%A5/mojolicious", "path")

    # to_dir
    path = Pyjo.Path.new('/i/%E2%99%A5/mojolicious').to_dir()
    is_ok(path, "/i/%E2%99%A5/", "path")

    path = Pyjo.Path.new('i/%E2%99%A5/mojolicious').to_dir()
    is_ok(path, "i/%E2%99%A5/", "path")

    # to_route
    path = Pyjo.Path.new('/i/%E2%99%A5/mojolicious').to_route()
    is_ok(path, u"/i/♥/mojolicious", "path")

    path = Pyjo.Path.new('i/%E2%99%A5/mojolicious').to_route()
    is_ok(path, u"/i/♥/mojolicious", "path")

    # to_str
    path = Pyjo.Path.new('/i/%E2%99%A5/pyjo').to_str()
    is_ok(path, "/i/%E2%99%A5/pyjo", "path")

    path = Pyjo.Path.new('i/%E2%99%A5/pyjo').to_str()
    is_ok(path, "i/%E2%99%A5/pyjo", "path")

    # trailing_slash
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    trailing_slash = path.trailing_slash
    is_ok(trailing_slash, False, "trailing_slash")
    path.trailing_slash = True
    trailing_slash = path.trailing_slash
    is_ok(trailing_slash, True, "trailing_slash")

    done_testing()
