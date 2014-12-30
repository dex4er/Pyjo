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
    b, punycode_decode, punycode_encode, url_escape, url_unescape
)


class Pyjo_URL(Pyjo.Base.String.object):
    """::

        url = Pyjo.URL.new()
        url = Pyjo.URL.new('http://127.0.0.1:3000/foo?f=b&baz=2#foo')

    Construct a new :mod:`Pyjo.URL` object and :meth:`parse` URL if necessary.
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

    _base = None
    _path = None
    _query = None

    def __init__(self, *args, **kwargs):
        """::

            url = Pyjo.URL.new()
            url = Pyjo.URL.new('http://127.0.0.1:3000/foo?f=b&baz=2#foo');

        Construct a new :mod:`Pyjo.URL` object and :meth:`parse` URL if necessary.
        """
        if len(args) == 1:
            self.parse(args[0])
        elif args:
            self.set(*args)
        elif kwargs:
            self.set(**kwargs)

    @property
    def authority(self):
        """::

            authority = url.authority
            url.authority = 'root:%E2%99%A5@localhost:8080'

        Authority part of this URL. ::

            # "root:%E2%99%A5@xn--n3h.net:8080"
            Pyjo.URL.new('http://root:♥@☃.net:8080/test').authority

            # "root@example.com"
            Pyjo.URL.new('http://root@example.com/test').authority
        """
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
            self.ihost = host.decode('utf-8')
        else:
            self.host = host.decode('ascii')

        return self

    @property
    def base(self):
        """::

            base = url.base
            url.base = Pyjo.URL.new()

        Base of this URL, defaults to a :mod:`Pyjo.URL` object.
        """
        if self._base is None:
            self._base = Pyjo.URL.new()
        return self._base

    @base.setter
    def base(self, value):
        # TODO old path / new path
        self._base = Pyjo.URL.new(value)
        return self

    def clone(self):
        """::

            url2 = url.clone()

        Clone this URL.
        """
        clone = self.new()
        clone.fragment = self.fragment
        clone.host = self.host
        clone.port = self.port
        clone.scheme = self.scheme
        clone.userinfo = self.userinfo
        if self._base is not None:
            clone._base = self._base.clone()
        if self._path is not None:
            clone._path = self._path.clone()
        if self._query is not None:
            clone._query = self._query.clone()
        return clone

    @property
    def host_port(self):
        """::

            host_port = url.host_port

        Normalized version of :attr:`host` and :attr:`port`. ::

            # "xn--n3h.net:8080"
            Pyjo.URL.new('http://☃.net:8080/test').host_port

            # "example.com"
            Pyjo.URL.new('http://example.com/test').host_port
        """
        host = self.ihost
        port = self.port
        if port is not None:
            return '{0}:{1}'.format(host, port)
        else:
            return host

    @property
    def ihost(self):
        """::

            ihost = url.ihost
            url.ihost = 'xn--bcher-kva.ch'

        Host part of this URL in punycode format. ::

            # "xn--n3h.net"
            Pyjo.URL.new('http://☃.net').ihost

            # "example.com"
            Pyjo.URL.new('http://example.com').ihost
        """
        host = self.host

        if host is None:
            return

        if host != m(r'[^\x00-\x7f]'):
            return b(host, 'ascii').decode('ascii').lower()

        # Encode
        parts = map(lambda s: ('xn--' + punycode_encode(s).decode('ascii')) if s == m(r'[^\x00-\x7f]') else s, host.split('.'))
        return '.'.join(parts).lower()

    @ihost.setter
    def ihost(self, value):
        # Decode
        parts = map(lambda s: punycode_decode(s[4:]) if s == m(r'^xn--(.+)$') else s, value.split('.'))
        self.host = '.'.join(parts)
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
