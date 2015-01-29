# -*- coding: utf-8 -*-

"""
Pyjo.Content - HTTP content base class
======================================
::

    import Pyjo.Content

    class MyContent(Pyjo.Content.object):
        def body_contains(self):
            ...

        def sub body_size(self):
            ...

        def get_body_chunk(self):
            ....

:mod:`Pyjo.Content` is an abstract base class for HTTP content based on
:rfc:`7230` and
:rfc:`7231`.

Events
------

:mod:`Pyjo.Content` inherits all events from :mod:`Pyjo.EventEmitter` and can emit
the following new ones.

body
^^^^
::

    @content.on
    def body(content):
        ...

Emitted once all headers have been parsed and the body starts. ::

    @content.on
    def body(content):
        if content.headers.header('X-No-MultiPart'):
            content.auto_upgrade = False

drain
^^^^^
::

    @content.on
    def drain(content, offset):
        ...

Emitted once all data has been written. ::

    @content.on
    def drain(content, offset):
        content.write_chunk(time.time())

read
^^^^
::

    @content.on
    def read(content, bstring):
        ...

Emitted when a new chunk of content arrives. ::

    content.unsubscribe('read')

    @content.on
    def read(content, bstring):
        print("Streaming: {0}".format(bstring))
"""

import Pyjo.Base

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv, u


class Pyjo_Content(Pyjo.Base.object):
    """::
    """


new = Pyjo_Content.new
object = Pyjo_Content  # @ReservedAssignment
