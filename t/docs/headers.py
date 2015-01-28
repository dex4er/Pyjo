# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.Headers

    # Parse
    headers = Pyjo.Headers.new()
    isa_ok(headers, Pyjo.Headers.object, "headers")
    is_ok(headers, b"\x0d\x0a\x0d\x0a", "headers")
    headers.parse(b"Content-Length: 42\x0d\x0a")
    is_ok(headers, b"\x0d\x0a\x0d\x0a", "headers")
    headers.parse(b"Content-Type: text/html\x0d\x0a\x0d\x0a")
    is_ok(headers, b"Content-Length: 42\x0d\x0aContent-Type: text/html\x0d\x0a\x0d\x0a", "headers")
    is_ok(headers.content_length, b'42', "headers.content_length")
    is_ok(headers.content_type, b'text/html', "headers.content_type")

    # Build
    headers = Pyjo.Headers.new()
    isa_ok(headers, Pyjo.Headers.object, "headers")
    is_ok(headers, b"\x0d\x0a\x0d\x0a", "headers")
    headers.content_length = 42
    headers.content_type = 'text/plain'
    is_ok(headers.to_str(), "Content-Length: 42\x0d\x0aContent-Type: text/plain\x0d\x0a\x0d\x0a", "headers")

    # new
    headers = Pyjo.Headers.new("Content-Type: text/plain\x0d\x0a\x0d\x0a")
    is_ok(headers, "Content-Type: text/plain\x0d\x0a\x0d\x0a", "headers")

    # add
    headers = Pyjo.Headers.new()
    headers.set(vary='Accept').add('Vary', 'Accept-Encoding')
    is_ok(headers, "Vary: Accept\x0d\x0aVary: Accept-Encoding\x0d\x0a\x0d\x0a", "headers")

    # append
    headers = Pyjo.Headers.new()
    headers.append('Vary', 'Accept').to_str()
    is_ok(headers, "Vary: Accept\x0d\x0a\x0d\x0a", "headers")

    headers = Pyjo.Headers.new()
    headers.set(vary='Accept').append('Vary', 'Accept-Encoding').to_str()
    is_ok(headers, "Vary: Accept, Accept-Encoding\x0d\x0a\x0d\x0a", "headers")

    done_testing()
