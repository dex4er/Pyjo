# -*- coding: utf-8 -*-

"""
Pyjo.Message - HTTP message base class
======================================
::

    import Pyjo.Message

    class MyMessage(Pyjo.Message.object):

        def cookies(self):
            ...

        def extract_start_line(self, chunk):
            ...

        def get_start_line_chunk(self):
            ...

:mod:`Pyjo.Message` is an abstract base class for HTTP messages based on
:rfc:`7230`,
:rfc:`7231` and
:rfc:`2388`.

Events
------

:mod:`Pyjo.Message` inherits all events from :mod:`Pyjo.EventEmitter` and can emit
the following new ones.

finish
~~~~~~
::

    @msg.on
    def finish(msg):
        ...


Emitted after message building or parsing is finished. ::

    from Pyjo.Util import steady_time
    before = steady_time()

    @msg.on
    def finish(msg):
        msg.headers.header('X-Parser-Time', int(steady_time() - before))

progress
~~~~~~~~
::

    @msg.on
    def progress(msg, state, offset):
        ...

Emitted when message building or parsing makes progress. ::

    # Building
    @msg.on
    def progress(msg, state, offset):
        print("Building {0} at offset {1}".format(state, offset))

    # Parsing
    @msg.on
    def progress(msg, state, offset):
        length = msg.headers.content_length
        if length:
            size = msg.content.progress
            print("Progress: {0}%".format(100 if size == length
                                          else int(size / (length / 100))))

Classes
-------
"""

import Pyjo.Asset.Memory
import Pyjo.Content.Single
import Pyjo.DOM
import Pyjo.EventEmitter
import Pyjo.JSON.Pointer
import Pyjo.Parameters
import Pyjo.String.Mixin

from Pyjo.Base import lazy
from Pyjo.JSON import j
from Pyjo.Regexp import r
from Pyjo.Util import b, getenv, not_implemented, notnone


re_filename = r(r'[; ]filename="((?:\\"|[^"])*)"')
re_name = r(r'[; ]name="((?:\\"|[^;"])*)"')


class Pyjo_Message(Pyjo.EventEmitter.object, Pyjo.String.Mixin.object):
    """
    :mod:`Pyjo.Message` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and :mod:`Pyjo.String.Mixin`
    and implements the following new ones.
    """

    content = lazy(lambda self: Pyjo.Content.Single.new())
    """::

        content = msg.content
        msg.content = Pyjo.Content.Single.new()

    Message content, defaults to a :mod:`Pyjo.Content.Single` object.
    """

    default_charset = 'utf-8'
    """::

        charset = msg.default_charset
        msg.default_charset = 'utf-8'

    Default charset used by :attr:`text` and to extract data from
    ``application/x-www-form-urlencoded`` or ``multipart/form-data`` message body,
    defaults to ``utf-8``.
    """

    max_line_size = lazy(lambda self: getenv('PYJO_MAX_LINE_SIZE') or 8192)
    """::

        size = msg.max_line_size
        msg.max_line_size = 8192

    Maximum start-line size in bytes, defaults to the value of the
    ``PYJO_MAX_LINE_SIZE`` environment variable or ``8192`` (8KB).
    """

    max_message_size = lazy(lambda self: getenv('PYJO_MAX_MESSAGE_SIZE', 16777216))
    """::

        size = msg.max_message_size
        msg.max_message_size = 16777216

    Maximum message size in bytes, defaults to the value of the
    ``PYJO_MAX_MESSAGE_SIZE`` environment variable or ``16777216`` (16MB). Setting
    the value to ``0`` will allow messages of indefinite size. Note that increasing
    this value can also drastically increase memory usage, should you for example
    attempt to parse an excessively large message body with the :attr:`body_params`,
    :meth:`dom` or :meth:`json` methods.
    """

    version = '1.1'
    """::

        version = msg.version
        msg.version = '1.1'

    HTTP version of message, defaults to ``1.1``.
    """

    _body_params = None
    _buffer = lazy(lambda self: bytearray())
    _dom = None
    _error = lazy(lambda self: {})
    _finished = False
    _fixed = False
    _json = None
    _raw_size = 0
    _state = None

    @property
    def body(self):
        """::

            bytes = msg.body
            msg.body = b'Hello!'

        Slurp or replace :attr:`content`, :mod:`Mojo.Content.MultiPart` will be
        automatically downgraded to :mod:`Pyjo.Content.Single`.
        """
        content = self._downgrade_content()
        return content.asset.slurp()

    @body.setter
    def body(self, value):
        content = self._downgrade_content()
        return content.set(asset=Pyjo.Asset.Memory.new().add_chunk(value))

    @property
    def body_params(self):
        """::

            params = msg.body_params

        ``POST`` parameters extracted from ``application/x-www-form-urlencoded`` or
        ``multipart/form-data`` message body, usually a :mod:`Pyjo.Parameters` object. Note
        that this method caches all data, so it should not be called before the entire
        message body has been received. Parts of the message body need to be loaded
        into memory to parse ``POST`` parameters, so you have to make sure it is not
        excessively large, there's a 16MB limit by default. ::

            # Get POST parameter names and values
            params_dict = msg.body_params.to_dict()
        """
        if self._body_params:
            return self._body_params

        params = Pyjo.Parameters.new()
        self._body_params = params
        params.charset = self.content.charset or self.default_charset

        # "application/x-www-form-urlencoded"
        content_type = notnone(self.headers.content_type, '')
        if content_type.lower().find('application/x-www-form-urlencoded') >= 0:
            params.parse(self.content.asset.slurp())

        # "multipart/form-data"
        elif content_type.lower().find('multipart/form-data'):
            for name, value in self._parse_formdata():
                params.append((name, value),)

        return params

    @property
    def body_size(self):
        """::

            size = msg.body_size

        Content size in bytes.
        """
        return self.content.body_size

    def build_body(self):
        """::

            chunk = msg.build_body()

        Render whole body.
        """
        return self._build('get_body_chunk')

    def build_headers(self):
        """::

            chunk = msg.build_headers()

        Render all headers.
        """
        return self._build('get_header_chunk')

    def build_start_line(self):
        """::

            chunk = msg.build_start_line()

        Render start-line.
        """
        return self._build('get_start_line_chunk')

    def dom(self, pattern=None):
        """::

            dom = msg.dom()
            collection = msg.dom('a[href]')

        Retrieve message body from :attr:`text` and turn it into a :mod:`Pyjo.DOM` object,
        an optional selector can be used to call the method :meth:`Pyjo.DOM.find` on it
        right away, which then returns a :mod:`Pyjo.Collection` object. Note that this
        method caches all data, so it should not be called before the entire message
        body has been received. The whole message body needs to be loaded into memory
        to parse it, so you have to make sure it is not excessively large, there's a
        16MB limit by default. ::

            # Perform "find" right away
            print(msg.dom('h1, h2, h3').map('text').join("\n"))

            # Use everything else Mojo::DOM has to offer
            print(msg.dom.at('title').text)
            print(msg.dom.at('body').children().map('tag').uniq().join("\n"))
        """
        if self.content.is_multipart:
            return
        else:
            if self._dom is None:
                self._dom = Pyjo.DOM.new(self.text)
            dom = self._dom
            if pattern is None:
                return dom
            else:
                return dom.find(pattern)

    def error(self, **kwargs):
        """::

            err = msg.error
            msg = msg.error(message='Parser error')

        Get or set message error, an ``None`` return value indicates that there is no
        error. ::

            # Connection or parser error
            msg.error(message='Connection refused')

            # 4xx/5xx response
            msg.error(message='Internal Server Error', code=500)
        """
        if kwargs:
            self._error = kwargs
            self.finish()
        else:
            return self._error

    @not_implemented
    def extract_start_line(self, chunk):
        pass

    def finish(self):
        self._state = 'finished'
        if self._finished:
            return self
        else:
            self._finished = True
            return self.emit('finish')

    def fix_headers(self):
        # TODO
        self._fixed = True
        return self

    def get_body_chunk(self, offset):
        self.emit('progress', 'body', offset)
        chunk = self.content.get_body_chunk(offset)
        if chunk is not None and not len(chunk):
            self.finish()
        return chunk

    def get_header_chunk(self, offset):
        self.emit('progress', 'headers', offset)
        return self.fix_headers().content.get_header_chunk(offset)

    @not_implemented
    def get_start_line_chunk(self, offset):
        pass

    @property
    def header_size(self):
        return self.fix_headers().content.header_size

    @property
    def headers(self):
        return self.content.headers

    @property
    def is_finished(self):
        return self._state == 'finished'

    def json(self, pointer=None):
        if self.content.is_multipart():
            return

        if self._json is None:
            self._json = j(self.body)

        data = self._json
        if pointer:
            return Pyjo.JSON.Pointer.new(data).get(pointer)
        else:
            return data

    def parse(self, chunk=b''):
        if self._error:
            return self
        self._raw_size += len(chunk)
        self._buffer += chunk

        # Start-line
        if not self._state:
            # Check start-line size
            try:
                l = self._buffer.index(b"\x0a")
            except ValueError:
                l = len(self._buffer)
            if l > self.max_line_size:
                return self._limit('Maximum start-line size exceeded')

            if self.extract_start_line():
                self._state = 'content'

        # Content
        if self._state == 'content' or self._state == 'finished':
            self.content = self.content.parse(self._buffer)
            self._buffer = bytearray()

        # Check message size
        max_size = self.max_message_size
        if max_size and max_size < self._raw_size:
            return self._limit('Maximum message size exceeded')

        # Check header size
        if self.headers.is_limit_exceeded:
            return self._limit('Maximum header size exceeded')

        # Check buffer size
        if self.content.is_limit_exceeded:
            return self._limit('Maximum buffer size exceeded')

        if self.emit('progress', 'parse', 0).content.is_finished:
            return self.finish()
        else:
            return self

    @property
    def start_line_size(self):
        return len(self.build_start_line())

    def to_bytes(self):
        return self.build_start_line() + self.build_headers() + self.build_body()

    @property
    def text(self):
        body = self.body
        charset = self.content.charset or 'utf-8'
        try:
            return body.decode(charset)
        except:
            return body.decode('iso-8859-1')

    def _build(self, method):
        buf = b''
        offset = 0

        while True:
            # No chunk yet, try again
            chunk = getattr(self, method)(offset)
            if chunk is None:
                continue

            # End of part
            l = len(chunk)
            if not l:
                break

            offset += l
            buf += chunk

        return buf

    def _downgrade_content(self):
        # Downgrade multipart content
        if self.content.is_multipart:
            self.content = Pyjo.Content.Single.new()
        return self.content

    def _parse_formdata(self, upload=False):
        content = self.content

        if not content.is_multipart:
            return

        charset = content.charset or self.default_charset

        # Check all parts recursively
        parts = [content]
        while parts:
            part = parts.pop(0)
            if part.is_multipart:
                parts = part.parts + parts
                continue

            disposition = part.headers.content_disposition
            if not disposition:
                continue

            m = re_filename.search(disposition)
            filename = m.group(1) if m else None

            if upload and filename is None or not upload and filename is not None:
                continue

            m = re_name.search(disposition)
            name = m.group(1) if m else None
            if not upload:
                part = part.asset.slurp()

            # TODO charset

            yield name, part, filename


new = Pyjo_Message.new
object = Pyjo_Message  # @ReservedAssignment
