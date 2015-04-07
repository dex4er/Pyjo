# -*- coding: utf-8 -*-

"""
Pyjo.Cookie - HTTP cookie base class
====================================
::

    import Pyjo.Cookie

    class MyCookie(Pyjo.Cookie.object):
        def parse(self, string):
            ...

        def to_str(self):
            ...

:mod:`Pyjo.Cookie` is an abstract base class for HTTP cookie containers based on
:rfc:`6265`, like
:mod:`Pyjo.Cookie.Request` and :mod:`Pyjo.Cookie.Response`.

Classess
--------
"""

import Pyjo.Base
import Pyjo.String.Mixin


class Pyjo_Cookie(Pyjo.Base.object, Pyjo.String.Mixin.object):
    """
    :mod:`Pyjo.Cookie` inherits all methods from :mod:`Pyjo.Base` and :mod:`Pyjo.String.Mixin`
    and implements the following new ones.
    """


new = Pyjo_Cookie.new
object = Pyjo_Cookie  # @ReservedAssignment
