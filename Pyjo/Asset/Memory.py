# -*- coding: utf-8 -*-

"""
Pyjo.Asset.Memory - In-memory storage for HTTP content
======================================================
::

    import Pyjo.Asset.Memory

    mem = Pyjo.Asset.Memory.new()
    mem.add_chunk('foo bar baz')
    print(mem.slurp())

:mod:`Pyjo.Asset.Memory` is an in-memory storage backend for HTTP content.

Events
------

:mod:`Pyjo.Asset.Memory` inherits all events from :mod:`Pyjo.Asset` and can emit
the following new ones.

upgrade
^^^^^^^
::

    @content.on
    def upgrade(mem, file):
        ...

Emitted when asset gets upgraded to a :mod:`Pyjo.Asset.File` object. ::

    @content.on
    def upgrade(mem, file):
        file.tmpdir = '/tmp'
"""

import Pyjo.Asset

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv, u


class Pyjo_Asset_Memory(Pyjo.Asset.object):
    """::
    """


new = Pyjo_Asset_Memory.new
object = Pyjo_Asset_Memory  # @ReservedAssignment
