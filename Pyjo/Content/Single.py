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
"""

import Pyjo.Content

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv, u


class Pyjo_Content_Single(Pyjo.Content.object):
    """
    Methods
    -------
    """


new = Pyjo_Content_Single.new
object = Pyjo_Content_Single  # @ReservedAssignment
