# -*- coding: utf-8 -*-

r"""
Pyjo.Message.Request - HTTP request
===================================

::

    import Pyjo.Message.Request

    # Parse
    req = Pyjo.Message.Request.new()
    req.parse(b"GET /foo HTTP/1.0\x0d\x0a")
    req.parse(b"Content-Length: 12\x0d\x0a")
    req.parse(b"Content-Type: text/plain\x0d\x0a\x0d\x0a")
    req.parse(b'Hello World!');
    print(req.method)
    print(req.headers.content_type)
    print(req.body)

    # Build
    req = Pyjo.Message.Request.new()
    req.url.parse('http://127.0.0.1/foo/bar');
    req.method = 'GET'
    print(req)

:mod:`Pyjo.Message.Request` is a container for HTTP requests based on
:rfc:`7230`,
:rfc:`7231`,
:rfc:`7235` and
:rfc:`2817`.

Classes
-------
"""

import Pyjo.Cookie.Request
import Pyjo.Message
import Pyjo.String.Mixin
import Pyjo.URL

from Pyjo.Base import lazy
from Pyjo.Regexp import r
from Pyjo.Util import b, u


re_start_line = r(br'^\s*(.*?)\x0d?\x0a')
re_request = r(br'^(\S+)\s+(\S+)\s+HTTP\/(\d\.\d)$')


class Pyjo_Message_Request(Pyjo.Message.object, Pyjo.String.Mixin.object):
    """
    :mod:`Pyjo.Message.Request` inherits all attributes and methods from
    :mod:`Pyjo.Message` and :mod:`Pyjo.String.Mixin`
    and implements the following new ones.
    """

    method = 'GET'
    url = lazy(lambda self: Pyjo.URL.new())

    _proxy = None
    _start_buffer = None

    def __repr__(self):
        if self.method is not None:
            return "{0}.{1}({2})".format(self.__module__, self.__class__.__name__, repr(b('{0} {1} HTTP/{2}\r\n'.format(self.method, self.url, self.version), 'ascii') + bytes(self.content.headers) + bytes(self.content.asset.slurp())))
        else:
            return "{0}.{1}()".format(self.__module__, self.__class__.__name__)

    def clone(self):
        # Dynamic requests cannot be cloned
        content = self.content.clone()
        if content is not None:
            clone = self.new(content=content,
                             method=self.method,
                             url=self.url.clone(),
                             version=self.version)
            if self._proxy:
                clone._proxy = self._proxy.clone()
            return clone
        else:
            return

    @property
    def cookies(self):
        """::

            cookies = req.cookies

        Access request cookies, usually :mod:`Pyjo.Cookie.Request` objects. ::

            # Names of all cookies
            for cookie in req.cookies:
                print(cookie.name)
        """
        # Parse cookies
        headers = self.headers
        cookies = headers.set_cookie
        if cookies is not None:
            return Pyjo.Cookie.Request.parse(cookies)
        else:
            return

    def extract_start_line(self):
        # Ignore any leading empty lines
        m = re_start_line.search(self._buffer)
        if not m:
            return

        del self._buffer[:m.end()]
        m = re_request.search(m.group(1))

        if not m:
            return not self.error(message='Bad request start-line')

        self.method = u(m.group(1), 'ascii')
        self.version = u(m.group(3), 'ascii')
        url = self.url

        if self.method == 'CONNECT':
            url.authority = m.group(2)
        else:
            url.parse(m.group(2))

        return bool(url)

    def fix_headers(self):
        if self._fixed:
            return self

        super(Pyjo_Message_Request, self).fix_headers()

        # Host
        url = self.url
        headers = self.headers
        if not headers.host:
            headers.host = url.host_port

        # TODO
        return self

    def get_start_line_chunk(self, offset):
        if self._start_buffer is None:

            # Path
            url = self.url
            path = url.path_query
            if not path.startswith('/'):
                path = '/' + path

            # TODO CONNECT
            method = self.method.upper()

            # TODO Proxy

            self._start_buffer = b(method) + b' ' + b(path) + b' HTTP/' + b(self.version) + b'\x0d\x0a'

        self.emit('progress', 'start_line', offset)
        return self._start_buffer[offset:offset + 131072]

    def set_cookie(self, cookie):
        """::

            req = req.set_cookie(Pyjo.Message.Response.new(name='foo', value='bar'))
            req = req.set_cookie({'name': 'foo', 'value': 'bar'})

        Set message cookies, usually :mod:`Pyjo.Cookie.Response` object.
        """
        if isinstance(cookie, dict):
            value = Pyjo.Cookie.Request.new(**cookie)
        value = str(value)
        if self.headers.cookie is not None:
            self.headers.cookie += '; ' + value
        else:
            self.headers.cookie = value
        return self

    def to_bytes(self):
        return self.build_start_line() + self.build_headers() + self.build_body()


new = Pyjo_Message_Request.new
object = Pyjo_Message_Request  # @ReservedAssignment
