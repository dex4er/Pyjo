# -*- coding: utf-8 -*-

"""
Pyjo.Transaction - Transaction base class
=========================================

::

    import Pyjo.Transaction

    class MyTransaction(Pyjo.Transaction.object):

        def client_read(self):
            ...

        def client_write(self):
            ...

        def server_read(self):
            ...

        def server_write(self):
            ...

:mod:`Pyjo.Transaction` is an abstract base class for transactions.

Classes
-------
"""

import Pyjo.EventEmitter
import Pyjo.Message.Request
import Pyjo.Message.Response

from Pyjo.Base import lazy
from Pyjo.Util import not_implemented


class Pyjo_Transaction(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Transaction` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    local_address = None
    local_port = None
    remote_address = None
    remote_port = None
    req = lazy(lambda self: Pyjo.Message.Request.new())
    res = lazy(lambda self: Pyjo.Message.Response.new())

    _connection = None
    _state = None

    @not_implemented
    def client_read(self):
        pass

    @not_implemented
    def client_write(self):
        pass

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = value
        self.emit('connection', value)

    @property
    def is_finished(self):
        return self._state == 'finished'

    @property
    def is_writing(self):
        if self._state is None:
            return True
        else:
            return self._state == 'write'


new = Pyjo_Transaction.new
object = Pyjo_Transaction  # @ReservedAssignment
