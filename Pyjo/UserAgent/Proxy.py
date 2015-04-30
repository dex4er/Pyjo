# -*- coding: utf-8 -*-

"""
Pyjo.UserAgent.Proxy - User agent proxy manager
===============================================
::

    import Pyjo.UserAgent.Proxy

    proxy = Pyjo.UserAgent.Proxy.new()
    proxy.detect()
    print(proxy.http)

:mod:`Pyjo.UserAgent.Proxy` manages proxy servers for :mod:`Pyjo.UserAgent`.

Classes
-------
"""

import Pyjo.Base


class Pyjo_UserAgent_Proxy(Pyjo.Base.object):
    """
    :mod:`Pyjo.UserAgent.Proxy` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """


new = Pyjo_UserAgent_Proxy.new
object = Pyjo_UserAgent_Proxy  # @ReservedAssignment
