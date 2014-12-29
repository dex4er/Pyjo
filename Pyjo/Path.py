# -*- coding: utf-8 -*-

"""
Pyjo.Path - Path
================
::

    import Pyjo.Path

    # Parse
    path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')
    print(path[0])

    # Build
    path = Pyjo.Path.new('/i/♥')
    path.append('Pyjo')
    print(path)

:class:`Pyjo.Path` is a container for paths used by :class:`Pyjo.URL` and based on
:rfc:`3986`.
"""

import Pyjo.Base.String

from Pyjo.Util import url_escape


class Pyjo_Path(Pyjo.Base.String.object):
    """::

        path = Pyjo.Path.new()
        path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')

    Construct a new :class`Pyjo.Path` object and :meth:`parse` path if necessary.
    """

    charset = 'utf-8'
    leading_slash = None
    parts = []
    trailing_slash = None
    _path = None

    def __init__(self, path=None):
        super(Pyjo_Path, self).__init__()
        if path is not None:
            self.parse(path)

    def parse(self, path):
        self._path = path
        self.leading_slash = None
        self.parts = []
        self.trailing_slash = None
        return self

    def to_str(self):
        # Path
        charset = self.charset
        if self._path is not None:
            if charset:
                path = self._path.encode(charset).decode('iso-8859-1')
            else:
                path = self._path
            return url_escape(path, r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@/')

        # TODO Build path
        return


new = Pyjo_Path.new
object = Pyjo_Path  # @ReservedAssignment
