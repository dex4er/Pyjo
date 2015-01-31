# -*- coding: utf-8 -*-

"""
Pyjo.Content.Single - HTTP content
==================================

::

    import Pyjo.Content.Single

    single = Pyjo.Content.Single.new()
    single->parse(b"Content-Length: 12\\x0d\\x0a\\x0d\\x0aHello World!");
    print(single.headers.content_length)

:mod:`Pyjo.Content.Single` is a container for HTTP content based on
:rfc:`7230` and
:rfc:`7231`.

Events
------

:mod:`Pyjo.Content.Single` inherits all events from :mod:`Pyjo.Content` and can
emit the following new ones.

upgrade
^^^^^^^
::

    @content.on
    def upgrade(single, multi):
        ...

Emitted when content gets upgraded to a :mod:`Pyjo.Content.MultiPart` object. ::

    @content.on
    def upgrade(single, multi):
        g = multi.headers.content_type == m(r'multipart\/([^;]+)', 'i')
        if g:
            print('Multipart: ' + g[1])

Classes
-------
"""

import Pyjo.Asset.Memory
import Pyjo.Content
import Pyjo.Mixin.String

from Pyjo.Base import lazy
from Pyjo.Util import u


class Pyjo_Content_Single(Pyjo.Content.object, Pyjo.Mixin.String.object):
    """
    :mod:`Pyjo.Content.Single` inherits all attributes and methods from
    :mod:`Pyjo.Content` and implements the following new ones.
    """

    asset = lazy(lambda self: Pyjo.Asset.Memory.new(auto_upgrade=True))
    """::

        asset = single.asset
        single.asset = Pyjo.Asset.Memory.new()

    The actual content, defaults to a :mod:`Pyjo.Asset.Memory` object with
    :attr:`Pyjo.Asset.Memory.auto_upgrade` enabled.
    """

    _read = None

    def __init__(self, *args, **kwargs):
        """::

            single = Pyjo.Content.Single.new()

        Construct a new :mod:`Pyjo.Content.Single` object and subscribe to ``read``
        event with default content parser.
        """
        super(Pyjo_Content_Single, self).__init__(*args, **kwargs)
        self._read = self.on(lambda content, chunk: content.set(asset=content.asset.add_chunk(chunk)), 'read')

    def get_body_chunk(self, offset):
        """::

            bstring = single.get_body_chunk(0)

        Get a chunk of content starting from a specific position.
        """
        if self._dynamic:
            return self.generate_body_chunk(offset)
        else:
            return self.asset.get_chunk(offset)

    def to_str(self):
        return u(self.get_header_chunk(0), 'ascii') + u(self.get_body_chunk(0), 'ascii')


new = Pyjo_Content_Single.new
object = Pyjo_Content_Single  # @ReservedAssignment
