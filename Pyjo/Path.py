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
    _parts = None
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

    def canonicalize(self):
        """::

            path = path.canonicalize()

        Canonicalize path. ::

            # "/foo/baz"
            Pyjo.Path.new('/foo/./bar/../baz').canonicalize()

            # "/../baz"
            Pyjo.Path.new('/foo/../bar/../../baz').canonicalize()
        """
        parts = self.parts
        i = 0
        while i < len(parts):
            if parts[i] == '.' or parts[i] == '':
                parts.pop(i)
            elif i < 1 or parts[i] != '..' or parts[i - 1] == '..':
                i += 1
            else:
                i -= 1
                parts.pop(i)
                parts.pop(i)

        if not parts:
            self.trailing_slash = False

        return self

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

    def contains(self, prefix):
        """::

            boolean = path.contains(u'/i/♥/pyjo')

        Check if path contains given prefix. ::

            # True
            Pyjo.Path.new('/foo/bar').contains('/')
            Pyjo.Path.new('/foo/bar').contains('/foo')
            Pyjo.Path.new('/foo/bar').contains('/foo/bar')

            # False
            Pyjo.Path.new('/foo/bar').contains('/f')
            Pyjo.Path.new('/foo/bar').contains('/bar')
            Pyjo.Path.new('/foo/bar').contains('/whatever')
        """
        if prefix == '/':
            return True
        else:
            path = self.to_route()
            return len(path) >= len(prefix) \
                and path.startswith(prefix) \
                and (len(path) == len(prefix) or path[len(prefix)] == '/')

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

    def merge(self, path):
        """::

            path = path.merge('/foo/bar')
            path = path.merge('foo/bar')
            path = path.merge(Pyjo.Path.new('foo/bar'))

        Merge paths. Note that this method will normalize both paths if necessary and
        that ``%2F`` will be treated as ``/`` for security reasons. ::

            # "/baz/yada"
            Pyjo.Path.new('/foo/bar').merge('/baz/yada')

            # "/foo/baz/yada"
            Pyjo.Path.new('/foo/bar').merge('baz/yada')

            # "/foo/bar/baz/yada"
            Pyjo.Path.new('/foo/bar/').merge('baz/yada')
        """
        # Replace
        if path.startswith('/'):
            return self.parse(path)

        # Merge
        if not self.trailing_slash:
            self.parts.pop()

        path = self.new(path)
        self.parts += path.parts

        self._trailing_slash = path._trailing_slash

        return self

    def parse(self, path):
        """::

            path = path.parse('/foo%2Fbar%3B/baz.html')

        Parse path.
        """
        self._path = path

        self._parts = None
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

    def to_abs_str(self):
        """::

            str = path.to_abs_str()

        Turn path into an absolute string. ::

            # "/i/%E2%99%A5/pyjo"
            Pyjo.Path.new('/i/%E2%99%A5/pyjo').to_abs_str()
            Pyjo.Path.new('i/%E2%99%A5/pyjo').to_abs_str()
        """
        path = self.to_str()
        if not path.startswith('/'):
            path = '/' + path
        return path

    def to_dir(self):
        """::

            dir = route.to_dir()

        Clone path and remove everything after the right-most slash. ::

            # "/i/%E2%99%A5/"
            Pyjo.Path.new('/i/%E2%99%A5/pyjo').to_dir()

            # "i/%E2%99%A5/"
            Pyjo.Path.new('i/%E2%99%A5/pyjo').to_dir()
        """
        clone = self.clone()
        if not clone.trailing_slash:
            clone.parts.pop()
        clone.trailing_slash = bool(clone.parts)
        return clone

    def to_route(self):
        """::

            route = path.to_route()

        Turn path into a route. ::

            # "/i/♥/pyjo"
            Pyjo.Path.new('/i/%E2%99%A5/pyjo').to_route()
            Pyjo.Path.new('i/%E2%99%A5/pyjo').to_route()
        """
        clone = self.clone()
        route = '/' + '/'.join(clone.parts)
        if clone._trailing_slash:
            route += '/'
        return route

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

        if self._parts:
            parts = self._parts
            if charset:
                parts = map(lambda p: p.encode(charset).decode('iso-8859-1'), parts)
            path = '/'.join(map(lambda p: url_escape(p, r'^A-Za-z0-9\-._~!$&\'()*+,;=:@'), parts))
        else:
            path = ''

        if self._leading_slash:
            path = '/' + path

        if self._trailing_slash:
            path = path + '/'

        return path

    def _parse(self, name, *args):
        if self._parts is None:
            path = url_unescape(self._path if self._path is not None else '')
            self._path = None

            charset = self.charset

            if charset:
                path = path.decode(charset)

            path, count, _ = path == s(r'^/', '')
            self._leading_slash = bool(count)

            path, count, _ = path == s(r'/$', '')
            self._trailing_slash = bool(count)

            if path == '':
                self._parts = []
            else:
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
