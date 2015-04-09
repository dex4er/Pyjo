# -*- coding: utf-8 -*-

"""
Pyjo.Date - HTTP date
=====================

    import Pyjo.Date

    # Parse
    date = Pyjo.Date.new('Sun, 06 Nov 1994 08:49:37 GMT')
    print(date.epoch)

    # Build
    date = Pyjo.Date.new(steady_time() + 60)
    print(date)

:mod:`Pyjo.Date` implements HTTP date and time functions based on
:rfc:`7230`,
:rfc:`7231` and
:rfc:`3339`.

Classes
-------
"""

import Pyjo.Base
import Pyjo.String.Mixin


class Pyjo_Date(Pyjo.Base.object, Pyjo.String.Mixin.object):
    """
    :mod:`Pyjo.Date` inherits all attributes and methods from
    :mod:`Pyjo.Base` and :mod:`Pyjo.String.Mixin` and implements the following new ones.
    """

    def __bool__(self):
        """::

            boolean = bool(params)

        Always true. (Python 3.x)
        """
        return True

    def __nonzero__(self):
        """::

            boolean = bool(params)

        Always true. (Python 2.x)
        """
        return True


new = Pyjo_Date.new
object = Pyjo_Date  # @ReservedAssignment
