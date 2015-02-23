# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent.Transactor - User agent transactor
=================================================

::

    import Pyjo.UserAgent.Transactor

    # Simple GET request
    t = Pyjo.UserAgent.Transactor.new()
    print(t.tx('GET', 'http://example.com').req)

    # PATCH request with "Do Not Track" header and content
    print(t.tx('PATCH', 'example.com', headers={'DNT': 1}, data='Hi!').req)

    # POST request with form-data
    print(t.tx('POST', 'example.com', form={'a': 'b'}).req)

    # PUT request with JSON data
    print(t.tx('PUT', 'example.com', json={'a': 'b'}).req)

:mod:`Pyjo.UserAgent.Transactor` is the transaction building and manipulation
framework used by :mod:`Pyjo.UserAgent`.

Classes
-------
"""

import Pyjo.Base
import Pyjo.Transaction.HTTP
import Pyjo.URL

from Pyjo.Base import lazy
from Pyjo.JSON import encode_json
from Pyjo.Regexp import m
from Pyjo.Util import b


class Pyjo_UserAgent_Transactor(Pyjo.Base.object):
    """
    :mod:`Pyjo.UserAgent.Transactor` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """

    generators = lazy(lambda self: {'data': self._data, 'form': self._form, 'json': self._json})
    name = 'Pyjo (Python)'

    def endpoint(self, tx):
        # Basic endpoint
        req = tx.req
        url = req.url
        proto = url.protocol or 'http'
        host = url.ihost
        port = url.port or (443 if proto == 'https' else 80)

        # TODO Proxy for normal HTTP requests

        return proto, host, port

    def peer(self, tx):
        proto, host, port = self.endpoint(tx)
        return self._proxy(tx, proto, host, port)

    def redirect(self, old):
        # Commonly used codes
        res = old.res
        code = res.code or 0
        if code not in [301, 302, 303, 307, 308]:
            return

        # Fix location without authority and/or scheme
        location = res.headers.location
        if not location:
            return

        location = Pyjo.URL.new(location)
        if not location.is_abs():
            location = location.base(old.req.url).to_abs()
        proto = location.protocol
        if proto != 'http' and proto != 'https':
            return

        # Clone request if necessary
        new = Pyjo.Transaction.HTTP.new()
        req = old.req
        if code == 307 or code == 308:
            clone = req.clone()
            if not clone:
                return
            new.req = clone
        else:
            method = req.method.upper()
            headers = new.req.set(method='GET' if method == 'POST' else method) \
                .content.set(headers=req.headers.clone()).headers
            for n in filter(lambda n: n.lower().startswith('content-'), headers.names):
                headers.remove(n)

        headers = new.req.set(url=location).headers
        for n in ['Authorization', 'Cookie', 'Host', 'Referer']:
            headers.remove(n)

        new.previous = old
        return new

    def tx(self, method, url, headers={}, **kwargs):
        # Method and URL
        tx = Pyjo.Transaction.HTTP.new()
        req = tx.req
        req.method = method
        if str(url) != m(r'^/|://'):
            url = 'http://' + str(url)
        if isinstance(url, Pyjo.URL.object):
            req.url(url)
        else:
            req.url.parse(url)

        # Headers (we identify ourselves and accept gzip compression)
        h = req.headers
        if headers:
            h.from_dict(headers)
        if not h.user_agent:
            h.useragent = self.name
        if not h.accept_encoding:
            h.accept_encoding = 'gzip'

        # Generator
        generators = list(set(self.generators) & set(kwargs))
        if len(generators) == 1:
            g = generators[0]
            self.generators[g](tx, kwargs[g])

        # TODO Body

        return tx

    def _data(self, tx, data):
        tx.req.body = b(data)

    def _form(self, tx, data):
        raise Exception(self, tx, data);

    def _json(self, tx, data):
        tx.req.body = encode_json(data)
        self._type(tx.req.headers, 'application/json')
        return tx

    def _proxy(self, tx, proto, host, port):
        # TODO Update with proxy information
        return proto, host, port

    def _type(self, headers, content_type):
        if not headers.content_type:
            headers.content_type = content_type


new = Pyjo_UserAgent_Transactor.new
object = Pyjo_UserAgent_Transactor  # @ReservedAssignment
