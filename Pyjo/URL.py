# -*- coding: utf-8 -*-

"""
Pyjo.URL- Uniform Resource Locator
==================================
::

    import Pyjo.URL

    # Parse
    url = Pyjo.URL.new('http://sri:foobar@example.com:3000/foo/bar?foo=bar#23')
    print(url.scheme)
    print(url.userinfo)
    print(url.host)
    print(url.port)
    print(url.path)
    print(url.query)
    print(url.fragment)

    # Build
    url = Pyjo.URL.new()
    url.scheme = 'http'
    url.userinfo = 'sri:foobar'
    url.host = 'example.com'
    url.port = 3000
    url.path = '/foo/bar'
    url.query.param('foo', 'bar')
    url.fragment = 23
    print(url)

:mod:`Pyjo.URL` implements a subset of
:rfc:`3986`,
:rfc:`3987` and the
`URL Living Standard <https://url.spec.whatwg.org>`_ for Uniform Resource
Locators with support for IDNA and IRIs.
"""

import Pyjo.Base.String
import Pyjo.Parameters
import Pyjo.Path

from Pyjo.Regexp import m, s
from Pyjo.Util import (
    b, lazy, punycode_decode, punycode_encode, url_escape, url_unescape
)


class Pyjo_URL(Pyjo.Base.String.object):
    """::

        url = Pyjo.URL.new()
        url = Pyjo.URL.new('http://127.0.0.1:3000/foo?f=b&baz=2#foo')

    Construct a new :mod:`Pyjo.URL` object and :meth:`parse` URL if necessary.
    """

    base = lazy(lambda self: Pyjo_URL())
    """::

        base = url.base
        url.base = Pyjo.URL.new()

    Base of this URL, defaults to a :mod:`Pyjo.URL` object.
    """

    fragment = None
    """::

        fragment = url.fragment
        url.fragment = u'♥pyjo♥'

    Fragment part of this URL.
    """

    host = None
    """::

        host = url.host
        url.host = '127.0.0.1'

    Host part of this URL.
    """

    port = None
    """::

        port = url.port
        url.port = 8080

    Port part of this URL.
    """

    scheme = None
    """::

        scheme = url.scheme
        url.scheme = 'http'

    Scheme part of this URL.

    """

    userinfo = None
    """::

        info = url.userinfo
        url.userinfo = u'root:♥'

    Userinfo part of this URL.
    """

    _path = None
    _query = None

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.parse(args[0])
        elif args:
            self.set(*args)
        elif kwargs:
            self.set(**kwargs)

    @property
    def authority(self):
        # Build authority
        authority = self.host_port
        if authority is None:
            return

        info = self.userinfo
        if info is None:
            return authority
        info = url_escape(info.encode('utf-8'), r'^A-Za-z0-9\-._~!$&\'()*+,;=:')

        return info + '@' + authority

    @authority.setter
    def authority(self, authority):
        if authority is None:
            return self

        # Userinfo
        (authority, found, g) = authority == s(r'^([^\@]+)\@', '')
        if found:
            self.userinfo = url_unescape(g[1]).decode('utf-8')

        # Port
        (authority, found, g) = authority == s(r':(\d+)$', '')
        if found:
            self.port = int(g[1])

        # Host
        host = url_unescape(authority.encode('utf-8'))
        if host == m(br'[^\x00-\x7f]'):
            self.ihost = host
        else:
            self.host = host.decode('ascii')

        return self

    @property
    def host_port(self):
        host = self.ihost
        port = self.port
        if port is not None:
            return '{0}:{1}'.format(host, port)
        else:
            return host

    @property
    def ihost(self):
        host = self.host

        if host is None:
            return

        if host != m(r'[^\x00-\x7f]'):
            return b(host).decode('ascii').lower()

        # Encode
        return '.'.join(map(lambda s: ('xn--' + punycode_encode(s)) if s == m(r'[^\x00-\x7f]') else s, host.split('.'))).lower()

    @ihost.setter
    def ihost(self, value):
        # Decode
        self.host = '.'.join(map(lambda s: punycode_decode(s) if s == m(r'^xn--(.+)$') else s, value.decode('utf-8').split('.')))
        return self

    def is_abs(self):
        return bool(self.scheme)

    def parse(self, url):
        g = url == m(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')
        if g:
            if g[2] is not None:
                self.scheme = g[2]
            if g[4] is not None:
                self.authority = g[4]
            if g[5] is not None:
                self.path = g[5]
            if g[7] is not None:
                self.query = g[7]
            if g[9] is not None:
                self.fragment = url_unescape(g[9]).decode('utf-8')
        return self

    @property
    def path(self):
        if self._path is None:
            self._path = Pyjo.Path.new()
        return self._path

    @path.setter
    def path(self, value):
        # TODO old path / new path
        self._path = Pyjo.Path.new(value)
        return self

    @property
    def path_query(self):
        query = self.query.to_str()
        if len(query):
            query = '?' + query
        else:
            query = ''
        return self.path.to_str() + query

    @property
    def protocol(self):
        scheme = self.scheme

        if scheme is None:
            return ''

        return scheme.lower()

    @property
    def query(self):
        if self._query is None:
            self._query = Pyjo.Parameters.new()
        return self._query

    @query.setter
    def query(self, value):
        args = []
        kwargs = {}
        if hasattr(value, 'items'):
            kwargs = value
        elif isinstance(value, (list, tuple,)):
            args = value
        else:
            args = [value]
        self._query = Pyjo.Parameters.new(*args, **kwargs)
        return self

    def to_str(self):
        # Scheme
        url = ''
        proto = self.protocol

        if proto:
            url += proto + ':'

        # Authority
        authority = self.authority

        if authority is not None:
            url += '//' + authority

        # Path and query
        path = self.path_query

        if not authority or path == '' or path == m(r'^[/?]'):
            url += path
        else:
            url += '/' + path

        # Fragment
        fragment = self.fragment

        if fragment is None:
            return url

        return url + '#' + url_escape(fragment.encode('utf-8'), r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@\/?')


new = Pyjo_URL.new
object = Pyjo_URL  # @ReservedAssignment
