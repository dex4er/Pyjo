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
import Pyjo.Parameters
import Pyjo.Transaction.HTTP
import Pyjo.URL

from Pyjo.Base import lazy
from Pyjo.JSON import encode_json
from Pyjo.Regexp import m
from Pyjo.Util import b, notnone


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
        if not location.is_abs:
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
            self.generators[g](tx, **kwargs)

        # TODO Body

        return tx

    def _data(self, tx, data, **kwargs):
        tx.req.body = b(data)

    def _form(self, tx, form, **kwargs):
        # Check for uploads and force multipart if necessary
        req = tx.req
        headers = req.headers
        multipart = 'multipart/form-data' in notnone(headers.content_type, '').lower()
        for value in [v for l in map(lambda v: v if isinstance(v, (list, tuple)) else (v,), form.values()) for v in l]:
            if isinstance(value, dict):
                multipart = True
                break

        # Multipart
        if multipart:
            parts = self._multipart(kwargs['charset'], form)
            req.content = Pyjo.Content.MultiPart.new(headers=headers, parts=parts)
            self._type(headers, 'multipart/form-data')
            return tx

        # Query parameters or urlencoded
        p = Pyjo.Parameters.new(**form)
        if 'charset' in kwargs:
            p.charset = kwargs['charset']
        method = req.method.upper()
        if method == 'GET' or method == 'HEAD':
            req.url.query = p
        else:
            req.body = p.to_bytes()
            self._type(headers, 'application/x-www-form-urlencoded')

        return tx

    def _json(self, tx, json, **kwargs):
        tx.req.body = encode_json(json)
        self._type(tx.req.headers, 'application/json')
        return tx

    def _multipart(self, charset, form):
        raise Exception(self, charset, form)

    def _proxy(self, tx, proto, host, port):
        # TODO Update with proxy information
        return proto, host, port

    def _type(self, headers, content_type):
        if not headers.content_type:
            headers.content_type = content_type


new = Pyjo_UserAgent_Transactor.new
object = Pyjo_UserAgent_Transactor  # @ReservedAssignment
