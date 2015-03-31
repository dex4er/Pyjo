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

from Pyjo.Base import lazy


class Pyjo_Upload(Pyjo.Base.object):
    """
    :mod:`Pyjo.Upload` inherits all attributes and methods from
    :mod:`Pyjo.Base` and implements the following new ones.
    """

    asset = lazy(lambda self: Pyjo.Asset.File.new())
    """::

        asset = upload.asset
        upload.asset = Pyjo.Asset.File.new()

    Asset containing the uploaded data, usually a :mod:`Pyjo.Asset.File` or
    :mod:`Pyjo.Asset.Memory` object.
    """

    filename = None
    """::

        filename = upload.filename
        upload.filename = 'foo.txt'

    Name of the uploaded file.
    """

    name = None
    """::

        name = upload.name
        upload.name = 'foo'

    Name of the upload.
    """

    headers = lazy(lambda self: Pyjo.Headers.new())
    """::

        headers = upload.headers
        upload.headers = Pyjo.Headers.new()

    Headers for upload, defaults to a :mod:`Pyjo.Headers` object.
    """

    def move_to(self, path):
        """::

            upload = upload.move_to('/home/pyjo/foo.txt')

        Move uploaded data into a specific file.
        """
        self.asset.move_to(path)
        return self

    @property
    def size(self):
        """::

            size = upload.size

        Size of uploaded data in bytes.
        """
        return self.asset.size

    def slurp(self):
        """::

            bstring = upload.slurp()

        Read all uploaded data at once.
        """
        return self.asset.slurp()


new = Pyjo_Upload.new
object = Pyjo_Upload  # @ReservedAssignment
