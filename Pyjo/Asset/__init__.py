# -*- coding: utf-8 -*-

"""
Pyjo.Asset - HTTP content storage base class
============================================
::

    import Pyjo.Asset

    class MyAsset(Pyjo.Asset.object):
        def add_chunk(self):
            ...

        def contains(self):
            ...

        def get_chunk(self):
            ....

        def move_to(self):
            ....

        def mtime(self):
            ....

        def size(self):
            ....

        def slurp(self):
            ....

:mod:`Pyjo.Asset` is an abstract base class for HTTP content storage.

Events
------

:mod:`Pyjo.Asset` inherits all events from :mod:`Pyjo.EventEmitter`.
"""

import Pyjo.Base

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv, u


class Pyjo_Asset(Pyjo.Base.object):
    """::
    """


new = Pyjo_Asset.new
object = Pyjo_Asset  # @ReservedAssignment
