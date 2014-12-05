# coding: utf-8

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.URL

    # Simple
    url = Pyjo.URL.new('HtTp://Example.Com')
    is_ok(url.scheme, 'HtTp', 'right scheme')
    is_ok(url.protocol, 'http', 'right protocol')
    is_ok(url.host, 'Example.Com', 'right host')
    is_ok(url.ihost, 'example.com', 'right internationalized host')
    is_ok(url.authority, 'example.com', 'right authority')
    is_ok(url, 'http://example.com', 'right format')

    # Advanced
    url = Pyjo.URL.new('https://sri:foobar@example.com:8080/x/index.html?monkey=biz&foo=1#/!%?@3')
    ok(url.is_abs, 'is absolute')
    is_ok(url.scheme, 'https', 'right scheme')
    is_ok(url.protocol, 'https', 'right protocol')
    is_ok(url.userinfo, 'sri:foobar', 'right userinfo')
    is_ok(url.host, 'example.com', 'right host')
    is_ok(url.port, '8080', 'right port')
    is_ok(url.authority, 'sri:foobar@example.com:8080', 'right authority')
    is_ok(url.path, '/x/index.html', 'right path')
    is_ok(url.query, 'monkey=biz&foo=1', 'right query')
    is_ok(url.path_query, '/x/index.html?monkey=biz&foo=1', 'right path and query')
    is_ok(url.fragment, '/!%?@3', 'right fragment')
    is_ok(url,
          'https://sri:foobar@example.com:8080/x/index.html?monkey=biz&foo=1#/!%?@3',
          'right format')
    url.path = '/index.xml'
    is_ok(url,
          'https://sri:foobar@example.com:8080/index.xml?monkey=biz&foo=1#/!%?@3',
          'right format')

    # Advanced userinfo and fragment roundtrip
    url = Pyjo.URL.new('ws://AZaz09-._~!$&\'()*+,;=:@localhost#AZaz09-._~!$&\'()*+,;=%:@/?')
    is_ok(url.scheme, 'ws', 'right scheme')
    is_ok(url.userinfo, 'AZaz09-._~!$&\'()*+,;=:', 'right userinfo')
    is_ok(url.host, 'localhost', 'right host')
    is_ok(url.fragment, 'AZaz09-._~!$&\'()*+,;=%:@/?', 'right fragment')
    is_ok(url,
          'ws://AZaz09-._~!$&\'()*+,;=:@localhost#AZaz09-._~!$&\'()*+,;=%:@/?',
          'right format')

    done_testing()
