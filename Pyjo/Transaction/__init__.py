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

from Pyjo.Base import lazy


class Pyjo_Transaction(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Transaction` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """


new = Pyjo_Transaction.new
object = Pyjo_Transaction  # @ReservedAssignment
