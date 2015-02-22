# -*- coding: utf-8 -*-

"""
Pyjo.Transaction.HTTP - HTTP transaction
========================================

::

    import Pyjo.Transaction.HTTP

    # Client
    tx = Pyjo.Transaction.HTTP.new()
    tx.req.method = 'GET'
    tx.req.url.parse('http://example.com')
    tx.req.headers.accept = 'application/json'
    print(tx.res.code)
    print(tx.res.headers.content_type)
    print(tx.res.body)
    print(tx.remote_address)

:mod:`Pyjo.Transaction.HTTP` is a container for HTTP transactions based on
:rfc:`7230` and
:rfc:`7231`.

Classes
-------
"""

import Pyjo.Transaction


class Pyjo_Transaction_HTTP(Pyjo.Transaction.object):
    """
    :mod:`Pyjo.Transaction.HTTP` inherits all attributes and methods from
    :mod:`Pyjo.Transaction` and implements the following new ones.
    """

    previous = None

    _delay = False
    _http_state = None
    _offset = None
    _state = None
    _towrite = None

    def client_read(self, chunk):
        # Skip body for HEAD request
        res = self.res
        if self.req.method.upper() == 'HEAD':
            res.content.skip_body = True
        if not res.parse(chunk).is_finished():
            return

        # Unexpected 1xx response
        if not res.is_status_class(100) or res.headers.upgrade:
            self._state = 'finished'
            return

        self.res(res.new()).emit('unexpected', res)
        leftovers = res.content.leftovers
        if not len(leftovers):
            return
        self.client_read(leftovers)

    def client_write(self):
        return self._write(False)

    @property
    def keep_alive(self):
        # TODO
        return False

    @property
    def redirects(self):
        redirects = []
        previous = self
        while True:
            previous = previous.previous
            if not previous:
                break
            redirects.insert(0, previous)
        return redirects

    def _body(self, msg, finish):
        # TODO
        return b''

    def _headers(self, msg, head):
        # Prepare header chunk
        buf = msg.get_header_chunk(self._offset)
        written = len(buf) if buf is not None else 0
        self._towrite -= written
        self._offset += written

        # Switch to body
        if self._towrite <= 0:
            self._offset = 0

            # Response without body
            if head and self.is_empty:
                self._state = 'finished'

            # Body
            else:
                self._http_state = 'body'
                self._towrite = 1 if msg.content.is_dynamic() else msg.body_size

        return buf

    def _start_line(self, msg):
        # Prepare start-line chunk
        buf = msg.get_start_line_chunk(self._offset)
        written = len(buf) if buf is not None else 0
        self._towrite -= written
        self._offset += written

        # Switch to headers
        if self._towrite <= 0:
            self._http_state = 'headers'
            self._towrite = msg.header_size
            self._offset = 0

        return buf

#         # Delayed
#         if buf is not None:
#             self._delay = False
#         else:
#             if self._delay:
#                 self._delay = False
#                 self._state = 'paused'
#             else:
#                 self._delay = True
#
#         # Finished
#         self._state = 'finished' if finish else 'read'

    def _write(self, server):
        # Client starts writing right away
        if not server and self._state is None:
            self._state = 'write'

        if self._state != 'write':
            return ''

        # Nothing written yet
        if self._offset is None:
            self._offset = 0
        if self._towrite is None:
            self._towrite = 0

        if server:
            msg = self.res
        else:
            msg = self.req

        if not self._http_state:
            # Connection header
            headers = msg.headers
            if not headers.connection:
                headers.connection = 'keep-alive' if self.keep_alive else 'close'

            # Switch to start-line
            self._http_state = 'start_line'
            self._written = msg.start_line_size

        # Start-line
        chunk = b''
        if self._http_state == 'start_line':
            chunk += self._start_line(msg)

        # Headers
        if self._http_state == 'headers':
            chunk += self._headers(msg, server)

        # Body
        if self._http_state == 'body':
            chunk += self._body(msg, server)

        return chunk


new = Pyjo_Transaction_HTTP.new
object = Pyjo_Transaction_HTTP  # @ReservedAssignment
