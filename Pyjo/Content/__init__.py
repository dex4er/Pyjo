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

Classess
--------
"""

import Pyjo.EventEmitter
import Pyjo.Headers

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import b, getenv, not_implemented, u

import zlib


class Pyjo_Content(Pyjo.EventEmitter.object):
    """
    """

    auto_decompress = None
    """::

        boolean = content.auto_decompress
        content.auto_decompress = boolean

    Decompress content automatically if :attr:`is_compressed` is true.
    """

    auto_relax = None
    """::

        boolean = content.auto_relax
        content.auto_relax = boolean

    Try to detect when relaxed parsing is necessary.
    """

    expect_close = False
    """::

        boolean = content.expect_close
        content.expect_close = boolean

    Expect a response that is terminated with a connection close.
    """

    headers = lazy(lambda self: Pyjo.Headers.new())
    """::

        headers = content.headers
        content.headers = Pyjo.Headers.new()

    Content headers, defaults to a :mod:`Pyjo.Headers` object.
    """

    max_buffer_size = int(getenv('PYJO_MAX_BUFFER_SIZE', 0)) or 262144

    max_leftover_size = int(getenv('PYJO_MAX_LEFTOVER_SIZE', 0)) or 262144
    """::

        size = content.max_leftover_size
        content.max_leftover_size = 1024

    Maximum size in bytes of buffer for pipelined HTTP requests, defaults to the
    value of the ``PYJO_MAX_LEFTOVER_SIZE` environment variable or ``262144``
    (256KB).
    """

    relaxed = False
    """::

        boolean = content.relaxed
        content.relaxed = boolean

    Activate relaxed parsing for responses that are terminated with a connection
    close.
    """

    skip_body = False
    """::

        boolean = content.skip_body
        content.skip_body = boolean

    Skip body parsing and finish after headers.
    """

    _body = False
    _buffer = b''
    _chunk_len = 0
    _chunk_state = None
    _dynamic = False
    _gz = None
    _gz_size = 0
    _header_buffer = None
    _header_size = 0
    _limit = False
    _pre_buffer = b''
    _raw_size = 0
    _real_size = 0
    _size = 0
    _state = None

    def build_body(self):
        """::

            str = content.build_body()

        Render whole body.
        """
        return self._build('get_body_chunk')

    def build_headers(self):
        """::

            str = content.build_headers()

        Render all headers.
        """
        return self._build('get_header_chunk')

    @property
    def charset(self):
        content_type = self.headers.content_type
        if content_type is None:
            content_type = ''
        g = content_type == m(r'charset\s*=\s*"?([^"\s;]+)"?', 'i')
        if g:
            return g[1]
        else:
            return

    @not_implemented
    def get_body_chunk(self, offset):
        """::

            bytes = content.get_body_chunk(0)

        Get a chunk of content starting from a specific position. Meant to be
        overloaded in a subclass.
        """
        pass

    def get_header_chunk(self, offset):
        """::

            bytes = content.get_header_chunk(13)

        Get a chunk of the headers starting from a specific position.
        """
        if self._header_buffer is None:
            self._header_buffer = self.headers.to_bytes()

        return self._header_buffer[offset:131072]

    @property
    def header_size(self):
        return len(self.build_headers())

    @property
    def is_chunked(self):
        return bool(self.headers.transfer_encoding)

    @property
    def is_compressed(self):
        if self.headers.content_encoding is None:
            return False
        else:
            return bool(self.headers.content_encoding == m(r'^gzip$', 'i'))

    @property
    def is_dynamic(self):
        return self._dynamic and self.headers.content_length is None

    @property
    def is_finished(self):
        return self._state == 'finished'

    @property
    def is_limit_exceeded(self):
        return self._limit

    @property
    def is_multipart(self):
        return

    def parse(self, chunk):
        # Headers
        self._parse_until_body(b(chunk, 'ascii'))
        if self._state == 'headers':
            return self

        # Chunked content
        if self.is_chunked and self._state != 'headers':
            self._parse_chunked()
            if self._chunk_state == 'finished':
                self._state = 'finished'

        # Not chunked, pass through to second buffer
        else:
            self._real_size += len(self._pre_buffer)
            if not (self.is_finished and len(self._buffer) > self.max_leftover_size):
                self._buffer += self._pre_buffer
            self._pre_buffer = b''

        # No content
        if self.skip_body:
            self._state = 'finished'
            return self

        # Relaxed parsing
        headers = self.headers
        length = headers.content_length
        if self.auto_relax and length is None or length == '':
            connection = headers.connection.lower() if headers.connection is not None else ''
            if connection == 'close' or (not connection and self.expect_close):
                self.relaxed = True

        # Chunked or relaxed content
        if self.is_chunked or self.relaxed:
            self._decompress(self._buffer)
            self._size += len(self._buffer)
            self._buffer = b''
            return self

        # Normal content
        if length is not None and length.isdigit():
            length = int(length)
        else:
            length = 0
        need = length - self._size
        if need > 0:
            chunk = self._buffer[:need]
            self._buffer = self._buffer[need:]
            self._decompress(chunk)
            self._size += len(chunk)
        if length <= self.progress:
            self._state = 'finished'

        return self

    @property
    def progress(self):
        state = self._state
        if not state:
            return 0
        if state == 'body' or state == 'finished':
            return self._raw_size - self._header_size
        else:
            return 0

    def _build(self, method):
        buf, offset = b'', 0
        while True:
            # No chunk yet, try again
            chunk = getattr(self, method)(offset)
            if chunk is None:
                continue

            l = len(chunk)
            if not l:
                break

            offset += l
            buf += chunk

        return buf

    def _decompress(self, chunk):
        # No compression
        if not self.auto_decompress or not self.is_compressed:
            return self.emit('read', chunk)

        # Decompress
        if self._gz is None:
            self._gz = zlib.decompressobj(16 + zlib.MAX_WBITS)
        gz = self._gz

        out = gz.decompress(chunk)
        l = len(out)

        if l > 0:
            self.emit('read', out)

        self._gz_size += l

        # Replace Content-Encoding with Content-Length
        if gz.eof:
            self.headers.content_length = self._gz_size
            self.headers.remove('Content-Encoding')

        # Check buffer size
        else:
            if len(gz.unconsumed_tail) > self.max_buffer_size:
                self._state = 'finished'
                self._limit = True

    def _parse_chunked(self):
        # Trailing headers
        if self._chunk_state == 'trailing_headers':
            return self._parse_chunked_trailing_headers()

        while True:
            l = len(self._pre_buffer)
            if not l:
                break

            # Start new chunk (ignore the chunk extension)
            if not self._chunk_len:
                self._pre_buffer, g = self._pre_buffer == s(br'^(?:\x0d?\x0a)?([0-9a-fA-F]+).*\x0a', '')
                if not g:
                    break
                self._chunk_len = int(g[1], 16)
                if self._chunk_len:
                    continue

                # Last chunk
                self._chunk_state = 'trailing_headers'
                break

            # Remove as much as possible from payload
            if self._chunk_len < l:
                l = self._chunk_len
            self._buffer += self._pre_buffer[0:l]
            self._pre_buffer = self._pre_buffer[l:]
            self._real_size += l
            self._chunk_len -= l

        # Trailing headers
        if self._chunk_state == 'trailing_headers':
            self._parse_chunked_trailing_headers()

        # Check buffer size
        if len(self._pre_buffer) > self.max_buffer_size:
            self._state = 'finished'
            self._limit = True

    def _parse_headers(self):
        pre_buffer = self._pre_buffer
        self._pre_buffer = b''
        headers = self.headers.parse(pre_buffer)
        if not headers.is_finished:
            return
        self._state = 'body'

        # Take care of leftovers
        leftovers = self._pre_buffer = headers.leftovers
        self._header_size = self._raw_size - len(leftovers)

    def _parse_chunked_trailing_headers(self):
        headers = self.headers.parse(self._pre_buffer)
        self._pre_buffer = b''
        if not headers.is_finished:
            return
        self._chunk_state = 'finished'

        # Take care of leftover and replace Transfer-Encoding with Content-Length
        self._buffer += headers.leftovers
        headers.remove('Transfer-Encoding')
        if not headers.content_length:
            headers.content_length = self._real_size

    def _parse_until_body(self, chunk):
        self._raw_size += len(chunk)
        self._pre_buffer += chunk
        if self._state is None:
            self._state = 'headers'
        if self._state == 'headers':
            self._parse_headers()
        if self._state != 'headers' and not self._body:
            self._body = True
            self.emit('body')


new = Pyjo_Content.new
object = Pyjo_Content  # @ReservedAssignment
