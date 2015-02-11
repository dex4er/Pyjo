"""
Pyjo.IOLoop.Stream
"""

import Pyjo.EventEmitter
import Pyjo.IOLoop

from Pyjo.Util import getenv

import socket
import weakref

from errno import EAGAIN, ECONNRESET, EINTR, EPIPE, EWOULDBLOCK


if getenv('PYJO_NO_TLS', 0):
    TLS = False
    TLS_WANT_ERROR = None
else:
    try:
        from ssl import SSLError
        TLS = True
        try:
            from ssl import SSLWantReadError, SSLWantWriteError
            TLS_WANT_ERROR = True
        except ImportError:
            TLS_WANT_ERROR = False
    except ImportError:
        TLS = None
        TLS_WANT_ERROR = None

if not TLS:
    SSLError = None.__class__
if not TLS_WANT_ERROR:
    SSLWantReadError = SSLWantWriteError = None.__class__


class Pyjo_IOLoop_Stream(Pyjo.EventEmitter.object):

    reactor = None
    handle = None

    _graceful = False
    _timeout = 15
    _buffer = b''
    _timer = None
    _paused = False

    def __init__(self, handle, **kwargs):
        super(Pyjo_IOLoop_Stream, self).__init__(handle=handle, **kwargs)
        if self.reactor is None:
            self.reactor = Pyjo.IOLoop.singleton().reactor

    def __del__(self):
        self.close()

    def close(self):
        reactor = self.reactor
        if not dir(reactor):
            return

        self.timeout = 0
        handle = self.handle
        self.handle = None
        if not dir(handle):
            return

        reactor.remove(handle)
        handle.close()

        return self.emit('close')

    def close_gracefully(self):
        if self.is_writing():
            self._graceful = True
            return self
        return self.close()

    def is_readable(self):
        self._again()
        if not self.handle:
            return None
        return self.handle and self.reactor.is_readable(self.handle)

    def is_writing(self):
        if not self.handle:
            return None
        return len(self._buffer) or self.has_subscribers('drain')

    def start(self):
        # Resume
        reactor = self.reactor
        if self._paused:
            self._paused = False
            return reactor.watch(self.handle, 1, self.is_writting())

        self = weakref.proxy(self)

        def cb_read_write(self, is_write):
            if dir(self):
                if is_write:
                    self._write()
                else:
                    self._read()

        reactor.io(lambda is_write: cb_read_write(self, is_write), self.set(timeout=self._timeout).handle)

    def stop(self):
        if not self._paused:
            self.reactor.watch(self.handle, 0, self.is_writing())
        self._paused = True

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        reactor = self.reactor
        if self._timer:
            reactor.remove(self._timer)
            self._timer = None

        self._timeout = value

        if not value:
            return

        self = weakref.proxy(self)

        def timeout_cb(self):
            if bool(dir(self)):
                self.emit('timeout').close()

        self._timer = reactor.timer(lambda: timeout_cb(self), value)

    def write(self, chunk, cb=None):
        self._buffer += chunk
        if cb:
            self.once(cb, 'drain')
        elif not len(self._buffer):
            return self
        if self.handle:
            self.reactor.watch(self.handle, not self._paused, 1)

        return self

    def _again(self):
        if self._timer:
            self.reactor.again(self._timer)

    def _error(self, e):
        # Retry
        if e.errno == EAGAIN or e.errno == EINTR or e.errno == EWOULDBLOCK:
            return

        if isinstance(e, (SSLWantReadError, SSLWantReadError)):
            return

        if isinstance(e, (SSLError,)) and e.strerror.startswith('The operation did not complete'):
            return

        # Closed
        if e.errno == ECONNRESET or e.errno == EPIPE:
            return self.close()

        # Error
        self.emit('error', e).close()

    def _read(self):
        readbuffer = b''
        try:
            readbuffer = self.handle.recv(131072)
        except socket.error as e:
            return self._error(e)
        if not readbuffer:
            return self.close()
        self.emit('read', readbuffer)._again()

    def _write(self):
        handle = self.handle
        if len(self._buffer):
            try:
                written = handle.send(self._buffer)
            except socket.error as e:
                self._error(e)
            self.emit('write', self._buffer[:written])
            self._buffer = self._buffer[written:]
            if not len(self._buffer):
                self.emit('drain')
            self._again()

        if self.is_writing():
            return
        if self._graceful:
            return self.close()
        if self.handle:
            self.reactor.watch(handle, not self._paused, 0)


new = Pyjo_IOLoop_Stream.new
object = Pyjo_IOLoop_Stream  # @ReservedAssignment
