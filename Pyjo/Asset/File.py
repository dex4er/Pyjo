# -*- coding: utf-8 -*-

"""
Pyjo.Asset.File - File storage for HTTP content
===============================================
::

    import Pyjo.Asset.File

    # Temporary file
    file = Pyjo.Asset.File.new()
    file.add_chunk('foo bar baz')
    if file.contains('bar'):
        print('File contains "bar")
    print(file.slurp())

    # Existing file
    file = Pyjo.Asset.File.new(path='/home/pyjo/foo.txt')
    file.move_to('/tmp/yada.txt')
    print(file.slurp())

:mod:`Pyjo.Asset.File` is an file storage backend for HTTP content.

Events
------

:mod:`Pyjo.Asset.File` inherits all events from :mod:`Pyjo.Asset`.

Classes
-------
"""

import Pyjo.Asset

from Pyjo.Base import lazy
from Pyjo.Util import b, getenv, md5_sum, notnone, slurp, steady_time, rand

import errno
import os
import tempfile


class Error(Exception):
    """
    Exception raised when can't write to asset.
    """
    pass


class Pyjo_Asset_File(Pyjo.Asset.object):
    """
    :mod:`Pyjo.Asset.File` inherits all attributes and methods from
    :mod:`Pyjo.Asset` and implements the following new ones.
    """

    cleanup = None
    """::

        boolean = file.cleanup
        file.cleanup = boolean

    Delete :attr:`path` automatically once the file is not used anymore.
    """

    handle = lazy(lambda self: self._init_handle())
    """::

        handle = file.handle
        file.handle = open('/home/pyjo/foo.txt', 'rb')

    Filehandle, created on demand.
    """

    path = None
    """::

        path = file.path
        file.path = '/home/pyjo/foo.txt'

    File path used to create :attr:`handle`, can also be automatically generated if
    necessary.
    """

    tmpdir = lazy(lambda self: getenv('PYJO_TMPDIR') or tempfile.gettempdir())
    """::

        tmpdir = file.tmpdir
        file.tmpdir = '/tmp'

    Temporary directory used to generate :attr:`path`, defaults to the value of the
    ``PYJO_TMPDIR`` environment variable or auto detection.
    """

    _content = b''

    def __del__(self):
        if self.cleanup and self.path is not None and self.handle:
            self.handle.close()
            if os.access(self.path, os.W_OK):
                os.unlink(self.path)

    def add_chunk(self, chunk=b''):
        """::

            file = file.add_chunk(b'foo bar baz')

        Add chunk of data.
        """
        if self.handle.write(chunk) is None:
            raise Error("Can't write to asset")

        return self

    def contains(self, bstring):
        """::

            position = file.contains(b'bar')

        Check if asset contains a specific string.
        """
        handle = self.handle
        handle.seek(self.start_range, os.SEEK_SET)

        # Calculate window size
        end = notnone(self.end_range, self.size)
        length = len(bstring)
        size = max(length, 131072)
        size = min(size, end - self.start_range)

        # Sliding window search
        offset = 0
        window = handle.read(length)
        start = len(window)

        while offset < end:
            # Read as much as possible
            diff = end - (start + offset)
            buf = handle.read(min(diff, size))
            read = len(buf)
            window += buf

            # Search window
            pos = window.find(bstring)
            if pos >= 0:
                return offset + pos

            if read == 0:
                return -1

            offset += read
            if offset == end:
                return -1

            window = window[read:]

        return -1

    def get_chunk(self, offset, maximum=131072):
        """::

            bstream = asset.get_chunk(offset)
            bstream = asset.get_chunk(offset, maximum)

        Get chunk of data starting from a specific position, defaults to a maximum
        chunk size of ``131072`` bytes (128KB).
        """
        offset += self.start_range
        handle = self.handle
        handle.seek(offset, os.SEEK_SET)

        end = self.end_range
        if end is not None:
            chunk = end + 1 - offset
            if chunk <= 0:
                return b''
            else:
                return handle.read(min(chunk, maximum))
        else:
            return handle.read(maximum)

    @property
    def is_file(self):
        """::

            true = file.is_file

        True.
        """
        return True

    def move_to(self, dst):
        """::

            file = file.move_to('/home/pyjo/bar.txt')

        Move asset data into a specific file and disable :attr:`cleanup`.
        """
        # Windows requires that the handle is closed
        self.handle.close()
        self.handle = None

        # Move file and prevent clean up
        src = self.path
        os.rename(src, dst)
        self.path = dst
        self.cleanup = False
        return self

    @property
    def mtime(self):
        """::

            mtime = file.mtime

        Modification time of asset.
        """
        return os.fstat(self.handle.fileno()).st_mtime

    @property
    def size(self):
        """::

            size = file.size

        Size of asset data in bytes. Reading the size flushes writing buffer.
        """
        self.handle.flush()
        return os.fstat(self.handle.fileno()).st_size

    def slurp(self):
        """::

            bstring = file.slurp()

        Read all asset data at once.
        """
        if self.path is None:
            return b''
        else:
            return slurp(self.path)

    def _init_handle(self):
        # Open existing file
        path = self.path
        if path is not None and os.path.isfile(path):
            handle = open(path, 'rb')
            return handle

        # Open new or temporary file
        base = os.path.join(self.tmpdir, 'pyjo.tmp')
        if path is not None:
            fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_EXCL | os.O_RDWR)
        else:
            name = base
            while True:
                try:
                    fd = os.open(name, os.O_APPEND | os.O_CREAT | os.O_EXCL | os.O_RDWR)
                except IOError as e:
                    if e.errno == errno.EEXIST:
                        name = '{0}.{1}'.format(base, md5_sum(b('{0}{1}{2}'.format(steady_time(), os.getpid(), rand()))))
                    else:
                        raise e
                else:
                    break

        self.path = name

        # Enable automatic cleanup
        if self.cleanup is None:
            self.cleanup = True

        return os.fdopen(fd, 'a+b')


new = Pyjo_Asset_File.new
object = Pyjo_Asset_File  # @ReservedAssignment
