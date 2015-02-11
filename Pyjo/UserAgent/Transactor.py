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
from Pyjo.Regexp import m


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
        # TODO gzip
        # if not h.accept_encoding:
        #     h.accept_encoding = 'gzip'

        generators = list(set(self.generators) & set(kwargs))
        if len(generators) == 1:
            g = generators[0]
            self.genertors[g](tx, kwargs[g])

        return tx

    def _data(self, tx, data):
        tx.req.body = data

    def _form(self, tx, data):
        raise Exception(self, tx, data);

    def _json(self, tx, data):
        raise Exception(self, tx, data);

    def _proxy(self, tx, proto, host, port):
        # TODO Update with proxy information
        return proto, host, port


new = Pyjo_UserAgent_Transactor.new
object = Pyjo_UserAgent_Transactor  # @ReservedAssignment
