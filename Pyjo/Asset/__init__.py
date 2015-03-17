# -*- coding: utf-8 -*-

"""
Pyjo.Asset - HTTP content storage base class
============================================
::

    import Pyjo.Asset

    class MyAsset(Pyjo.Asset.object):
        def add_chunk(self, chunk=b''):
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

import Pyjo.EventEmitter

from Pyjo.Util import not_implemented


class Pyjo_Asset(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Asset` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """

    end_range = None
    """::

        end = asset.end_range
        asset.end_range = 8

    Pretend file ends earlier.
    """

    start_range = 0
    """::

        start = asset.start_range
        asset.start_range = 3

    Pretend file starts later.
    """

    @not_implemented
    def add_chunk(self, chunk=b''):
        """::

            asset = asset.add_chunk('foo bar baz')

        Add chunk of data to asset. Meant to be overloaded in a subclass.
        """
        pass

    @not_implemented
    def get_chunk(self, offset, maximum=131072):
        """::

            bstream = asset.get_chunk(offset)
            bstream = asset.get_chunk(offset, maximum)

        Get chunk of data starting from a specific position, defaults to a maximum
        chunk size of ``131072`` bytes (128KB). Meant to be overloaded in a subclass.
        """
        pass

    @property
    @not_implemented
    def size(self):
        """::

            size = asset.size

        Size of asset data in bytes. Meant to be overloaded in a subclass.
        """
        pass

    @not_implemented
    def slurp(self):
        """::

            bstring = asset.slurp()

        Read all asset data at once. Meant to be overloaded in a subclass.
        """
        pass


new = Pyjo_Asset.new
object = Pyjo_Asset  # @ReservedAssignment
