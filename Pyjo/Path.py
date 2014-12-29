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
    path.append('pyjo')
    print(path)

:mod:`Pyjo.Path` is a container for paths used by :mod:`Pyjo.URL` and based on
:rfc:`3986`.
"""

import Pyjo.Base.String

from Pyjo.Regexp import s
from Pyjo.Util import url_escape, url_unescape


class Pyjo_Path(Pyjo.Base.String.object):
    """::

        path = Pyjo.Path.new()
        path = Pyjo.Path.new('/foo%2Fbar%3B/baz.html')

    Construct a new :mod`Pyjo.Path` object and :meth:`parse` path if necessary.
    """

    charset = 'utf-8'
    """::

        charset = path.charset
        path.charset = 'utf-8'

    Charset used for encoding and decoding, defaults to ``utf-8``. ::

        # Disable encoding and decoding
        path.charset = None
    """

    _leading_slash = False
    _path = None
    _parts = []
    _trailing_slash = False

    def __init__(self, path=None):
        super(Pyjo_Path, self).__init__()
        if path is not None:
            self.parse(path)

    def __iter__(self):
        """::

            for p in path:
                print(p)

        Iterator based on :attr:`parts`. Note that this will normalize the path and that ``%2F``
        will be treated as ``/`` for security reasons.
        """
        parts = self.parts
        for p in parts:
            yield p

    def __bool__(self):
        """::

            boolean = bool(params)

        Always true.
        """
        return True

    __nonzero__ = __bool__

    def clone(self):
        """::

            clone = path.clone()

        Clone path.
        """
        new_obj = type(self)()
        new_obj.charset = self.charset
        if self._parts:
            new_obj._parts = list(self._parts)
            new_obj._leading_slash = self._leading_slash
            new_obj._trailing_slash = self._trailing_slash
        else:
            new_obj._path = self._path
        return new_obj

    @property
    def leading_slash(self):
        """::

            boolean = path.leading_slash
            path.leading_slash = boolean

        Path has a leading slash. Note that this method will normalize the path and
        that ``%2F`` will be treated as ``/`` for security reasons.
        """
        return self._parse('leading_slash')

    @leading_slash.setter
    def leading_slash(self, value):
        self._parse('leading_slash', value)

    def parse(self, path):
        """::

            path = path.parse('/foo%2Fbar%3B/baz.html')

        Parse path.
        """
        self._path = path

        self._parts = []
        self._leading_slash = False
        self._trailing_slash = False

        return self

    @property
    def parts(self):
        """::

            parts = path.parts
            path.parts = ['foo', 'bar', 'baz']

        The path parts. Note that this method will normalize the path and that ``%2F``
        will be treated as ``/`` for security reasons. ::

            # Part with slash
            path.parts.append('foo/bar')
        """
        return self._parse('parts')

    @parts.setter
    def parts(self, value):
        self._parse('parts', value)

    def to_str(self):
        """::

            string = path.to_str()

        Turn path into a string. ::

            # "/i/%E2%99%A5/pyjo"
            Pyjo.Path.new('/i/%E2%99%A5/pyjo').to_str()

            # "i/%E2%99%A5/pyjo"
            Pyjo.Path.new('i/%E2%99%A5/pyjo').to_str()
        """
        # Path
        charset = self.charset

        if self._path is not None:
            if charset:
                path = self._path.encode(charset).decode('iso-8859-1')
            else:
                path = self._path
            return url_escape(path, r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@/')

        parts = self._parts

        if charset:
            parts = map(lambda p: p.encode(charset).decode('iso-8859-1'), parts)

        path = '/'.join(map(lambda p: url_escape(p, r'^A-Za-z0-9\-._~!$&\'()*+,;=:@'), parts))

        if self._leading_slash:
            path = '/' + path

        if self._trailing_slash:
            path = path + '/'

        return path

    def _parse(self, name, *args):
        if not self._parts:
            path = url_unescape(self._path if self._path is not None else '')
            self._path = None

            charset = self.charset

            if charset:
                path = path.decode(charset)

            path, count, _ = path == s(r'^/', '')
            self._leading_slash = bool(count)

            path, count, _ = path == s(r'/$', '')
            self._trailing_slash = bool(count)

            self._parts = path.split('/')

        if not args:
            return getattr(self, '_' + name)

        setattr(self, '_' + name, args[0])

    @property
    def trailing_slash(self):
        """::

            boolean = path.trailing_slash
            path.trailing_slash = boolean

        Path has a trailing slash. Note that this method will normalize the path and
        that ``%2F`` will be treated as ``/`` for security reasons.
        """
        return self._parse('trailing_slash')

    @trailing_slash.setter
    def trailing_slash(self, value):
        self._parse('trailing_slash', value)


new = Pyjo_Path.new
object = Pyjo_Path  # @ReservedAssignment
