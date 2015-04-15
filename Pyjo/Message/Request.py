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
from Pyjo.Util import b, b64_encode, notnone, u


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

    _params = None
    _proxy = None
    _start_buffer = None

    def __repr__(self):
        """::

            string = repr(req)

        String representation of an object shown in console.
        """
        if self.method is not None:
            return "{0}.new({1})".format(self.__module__, repr(b('{0} {1} HTTP/{2}\r\n'.format(self.method, self.url, self.version), 'ascii') + bytes(self.content.headers) + bytes(self.content.asset.slurp())))
        else:
            return "{0}.new()".format(self.__module__)

    def clone(self):
        """::

            clone = req.clone

        Clone request if possible, otherwise return ``None``.
        """
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

    def every_param(self, name):
        """::

            values = req.every_param('foo')

        Similar to :meth:`param`, but returns all values sharing the same name as an
        array reference.

            # Get first value
            print(req.every_param('foo')[0])
        """
        return self.params.every_param(name)

    def extract_start_line(self, buf):
        """::

            boolean = req.extract_start_line(buf)

        Extract request-line from string.
        """
        # Ignore any leading empty lines
        m = re_start_line.search(buf)
        if not m:
            return

        line = m.group(1)
        del buf[:m.end()]
        m = re_request.search(line)

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
        """::

            req = req.fix_headers()

        Make sure request has all required headers.
        """
        if self._fixed:
            return self

        super(Pyjo_Message_Request, self).fix_headers()

        # Host
        url = self.url
        headers = self.headers
        if not headers.host:
            headers.host = url.host_port

        # Basic authentication
        info = url.userinfo
        if info and not headers.authorization:
            headers.authorization = 'Basic ' + b64_encode(b(info), '')

        # Basic proxy authentication
        proxy = self.proxy
        if not proxy:
            return self

        info = proxy.userinfo
        if not info:
            return self

        if not headers.proxy_authorization:
            headers.authorization = 'Basic ' + b64_encode(b(info), '')

        return self

    def get_start_line_chunk(self, offset):
        """::

            chunk = req.get_start_line_chunk(offset)

        Get a chunk of request-line data starting from a specific position.
        """
        if self._start_buffer is None:

            # Path
            url = self.url
            path = url.path_query
            if not path.startswith('/'):
                path = '/' + path

            # CONNECT
            method = self.method.upper()
            if method == 'CONNECT':
                port = url.port or (443 if url.protocol == 'https' else 80)
                path = '{0}:{1}'.format(self.ihost, port)

            # Proxy
            elif self.proxy and url.protocol != 'https':
                if self.is_handshake:
                    path = url.clone().userinfo = None

            self._start_buffer = b("{0} {1} HTTP/{2}\x0d\x0a".format(method, path, self.version))

        self.emit('progress', 'start_line', offset)
        return self._start_buffer[offset:offset + 131072]

    @property
    def is_handshake(self):
        """::

            boolean = req.is_handshake

        Check ``Upgrade`` header for ``websocket`` value.
        """
        return notnone(self.headers.upgrade, '').lower() == 'websocket'

    @property
    def is_secure(self):
        """::

            boolean = req.is_secure

        Check if connection is secure.
        """
        url = self.url
        return (url.protocol or url.base.protocol) == 'https'

    @property
    def is_xhr(self):
        """::

            boolean = req.is_xhr

        Check ``X-Requested-With`` header for ``XMLHttpRequest`` value.
        """
        return notnone(self.headers.header('X-Requested-With'), '').lower().find('xmlhttprequest') >= 0

    def param(self, name):
        """::

            value = req.param('foo')

        Access ``GET`` and ``POST`` parameters extracted from the query string and
        ``application/x-www-form-urlencoded`` or ``multipart/form-data`` message body. If
        there are multiple values sharing the same name, and you want to access more
        than just the last one, you can use :meth:`every_param`. Note that this method
        caches all data, so it should not be called before the entire request body has
        been received. Parts of the request body need to be loaded into memory to parse
        ``POST`` parameters, so you have to make sure it is not excessively large,
        there's a 16MB limit by default.
        """
        return self.params.param(name)

    @property
    def params(self):
        """::

            params = req.params

        All ``GET`` and ``POST`` parameters extracted from the query string and
        ``application/x-www-form-urlencoded`` or ``multipart/form-data`` message body,
        usually a :mod:`Pyjo.Parameters` object. Note that this method caches all data, so
        it should not be called before the entire request body has been received. Parts
        of the request body need to be loaded into memory to parse ``POST`` parameters,
        so you have to make sure it is not excessively large, there's a 16MB limit by
        default. ::

            # Get parameter names and values
            params_dict = req.params.to_dict()
        """
        if not self._params:
            self._params = self.body_params.clone().append(self.query_params)
        return self._params

    def parse(self):
        """::

            req = req.parse('GET /foo/bar HTTP/1.1')
            req = req.parse(REQUEST_METHOD='GET')
            req = req.parse({'REQUEST_METHOD': 'GET'})

        Parse HTTP request chunks or environment hash.
        """
        ...

    @property
    def proxy(self):
        return

    @property
    def query_params(self):
        return self.url.query

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
