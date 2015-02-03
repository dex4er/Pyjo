# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent - Non-blocking I/O HTTP and WebSocket user agent
===============================================================

::

    import Pyjo.UserAgent

    # Say hello to the Unicode snowman with "Do Not Track" header
    ua = Pyjo.UserAgent.new()
    print(ua.get(u'www.☃.net?hello=there', headers={'DNT': 1}).res.body

    # Form POST with exception handling
    tx = ua.post('https://metacpan.org/search', form={'q': 'pyjo'})
    if tx.success:
        print(tx.res.body)
    else:
        err = tx.error
        if err.code:
            raise Exception('{0} response: {1}'.format(err.code, err.message))
        else:
            raise Exception('Connection error: {0}'.format(err.message))

:mod:`Pyjo.UserAgent` is a full featured non-blocking I/O HTTP.

Classes
-------
"""

import Pyjo.EventEmitter
import Pyjo.UserAgent.Transactor

from Pyjo.Base import lazy


class Pyjo_UserAgent(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.UserAgent` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    transactor = lazy(lambda self: Pyjo.UserAgent.Transactor.new())

    def build_tx(self, url, **kwargs):
        return self.transactor.tx(url, **kwargs)

    def get(self, url, **kwargs):
        """::

            tx = ua.get('example.com')
            tx = ua.get('http://example.com', headers={'Accept': '*/*'}, data='Hi!')
            tx = ua.get('http://example.com', headers={'Accept': '*/*'},
                        form={'a': 'b'})
            tx = ua.get('http://example.com', headers={'Accept': '*/*'},
                        json={'a': 'b'})

        Perform blocking ``GET`` request and return resulting
        :mod:`Pyjo.Transaction.HTTP` object, takes the same arguments as
        :meth:`Pyjo.UserAgent.Transactor.tx` (except for the ``GET`` method, which is
        implied). You can also append a callback to perform requests non-blocking. ::

            def cb(ua, tx):
                print(tx.res.body)

            tx = ua.get('http://example.com', cb=cb)

            if not Pyjo.IOLoop.is_running()
                Pyjo.IOLoop.start()
        """
        return self.start(self.build_tx('GET', url, **kwargs), kwargs.get('cb'))

    def start(self, tx, cb=None):
        ...


new = Pyjo_UserAgent.new
object = Pyjo_UserAgent  # @ReservedAssignment
