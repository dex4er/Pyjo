# -*- coding: utf-8 -*-

r"""
Pyjo.Content.MultiPart - HTTP multipart content
===============================================
::

    import Pyjo.Content.MultiPart

    multi = Pyjo.Content.MultiPart.new()
    multi.parse(b'Content-Type: multipart/mixed; boundary=---foobar')
    single = multi.parts[4]
    print(single.headers.content_length)

:mod:`Pyjo.Content.MultiPart` is a container for HTTP multipart content based on
:rfc:`7230`,
:rfc:`7231` and
:rfc:`2388`.

Events
------

:mod:`Pyjo.Content.MultiPart` inherits all events from :mod:`Pyjo.Content` and can
emit the following new ones.

part
^^^^^^^
::

    @multi.on
    def part(multi, single):
        ...

Emitted when a new :mod:`Pyjo.Content.Single` part starts.

    from Pyjo.Regexp import r

    @multi.on
    def part(multi, single):
        m = r('name="([^"]+)"').search(single.headers.content_disposition)
        if m:
            print("Fields: {0}".format(m.group(1))

Classes
-------
"""

import Pyjo.Content
import Pyjo.String.Mixin

from Pyjo.Base import lazy


class Pyjo_Content_MultiPart(Pyjo.Content.object, Pyjo.String.Mixin.object):
    """
    :mod:`Pyjo.Content.MultiPart` inherits all attributes and methods from
    :mod:`Pyjo.Content` and implements the following new ones.
    """


new = Pyjo_Content_MultiPart.new
object = Pyjo_Content_MultiPart  # @ReservedAssignment
