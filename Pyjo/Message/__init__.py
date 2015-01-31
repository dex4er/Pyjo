# -*- coding: utf-8 -*-

"""
Pyjo.Message - HTTP message base class
======================================

::

    import Pyjo.Message

    class MyMessage(Pyjo.Message.object):

        def cookies(self):
            ...

        def extract_start_line(self):
            ...

        def get_start_line_chunk(self):
            ...

:mod:`Pyjo.Message` is an abstract base class for HTTP messages based on
:rfc:`7230`,
:rfc:`7231` and
:rfc:`2388`.

Classes
-------
"""

import Pyjo.EventEmitter

from Pyjo.Base import lazy


class Pyjo_Message(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Message` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """


new = Pyjo_Message.new
object = Pyjo_Message  # @ReservedAssignment
