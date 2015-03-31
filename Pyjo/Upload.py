# -*- coding: utf-8 -*-

"""
Pyjo.Upload - Upload
====================
::

    import Pyjo.Upload

    upload = Pyjo.Upload.new()
    print(upload.filename)
    upload.move_to('/home/pyjo/foo.txt')

:mod:`Pyjo.Upload` is a container for uploaded files.

Classes
-------
"""

import Pyjo.Asset.File
import Pyjo.Base
import Pyjo.Headers


class Pyjo_Upload(Pyjo.Base.object):
    """
    :mod:`Pyjo.Upload` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """


new = Pyjo_Upload.new
object = Pyjo_Upload  # @ReservedAssignment
