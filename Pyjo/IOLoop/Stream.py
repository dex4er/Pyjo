"""
Pyjo.IOLoop.Stream
"""

import socket
import weakref

from errno import EAGAIN, ECONNRESET, EINTR, EPIPE, EWOULDBLOCK

import Pyjo.IOLoop

from Pyjo.EventEmitter import *


__all__ = ['Pyjo_IOLoop_Stream']


class Pyjo_IOLoop_Stream(Pyjo_EventEmitter):
    reactor = None

    _handle = None
    _grafeful = False
    _timeout = 15
    _buffer = b''
    _timer = None
    _paused = False

    def __init__(self, handle):
        self.reactor = Pyjo.IOLoop.singleton().reactor
        self._handle = handle

    def __del__(self):
        self.close()

    def close(self):
        reactor = self.reactor
        if not reactor:
            return

        self.timeout(0)
        handle = self._handle
        self._handle = None
        if not handle:
            return

        reactor.remove(handle)
        handle.close()

        self.emit('close')

    def close_gracefully(self):
        if self.is_writing():
            self.graceful = True
            return self.graceful
        self.close()

    def handle(self):
        return self._handle

    def is_readable(self):
        self._again()
        if not self._handle:
            return None
        return self._handle and self.reactor.is_readable(self._handle)

    def is_writing(self):
        if not self._handle:
            return None
        return len(self._buffer) or self.has_subscribers('drain')

    def start(self):
        # Resume
        reactor = self.reactor
        if self._paused:
            self._paused = False
            return reactor.watch(self.handle, 1, self.is_writting())

        self = weakref.proxy(self)

        def cb_read_write(is_write):
            if dir(self):
                if is_write:
                    self._write()
                else:
                    self._read()

        reactor.io(self.timeout(self._timeout)._handle, cb_read_write)

    def stop(self):
        if not self._paused:
            self.reactor.watch(self._handle, 0, self.is_writing())
        self._paused = True

    def timeout(self, timeout=None):
        if timeout is None:
            return self._timeout

        reactor = self.reactor
        if self._timer:
            reactor.remove(self._timer)
            self._timer = None

        self._timeout = timeout

        if not timeout:
            return

        self = weakref.proxy(self)

        def timeout_cb():
            if bool(dir(self)):
                self.emit('timeout').close()

        self._timer = reactor.timer(timeout, timeout_cb)

        return self

    def write(self, chunk, cb=None):
        self._buffer += chunk
        if cb:
            self.once('drain', cb)
        elif not len(self._buffer):
            return self
        if self._handle:
            self.reactor.watch(self._handle, not self._paused, 1)

        return self

    def _again(self):
        if self._timer:
            self.reactor.again(self._timer)

    def _error(self, e):
        # Retry
        if e.errno == EAGAIN or e.errno == EINTR or e.errno == EWOULDBLOCK:
            return

        # Closed
        if e.errno == ECONNRESET or e.errno == EPIPE:
            return self.close()

        # Error
        self.emit('error', e).close()

    def _read(self):
        readbuffer = b''
        try:
            readbuffer = self._handle.recv(131072)
        except socket.error as e:
            return self._error(e)
        if not readbuffer:
            return self.close()
        self.emit('read', readbuffer)._again()

    def _write(self):
        handle = self._handle
        if len(self._buffer):
            try:
                written = handle.send(self._buffer)
            except socket.error as e:
                self._error(e)
            self.emit('write', self._buffer[:written])
            self._buffer = self._buffer[written:]
            if not len(self._buffer):  # TODO once?
                self.emit('drain')
            self._again()

        if self.is_writing:
            return
        if self._graceful:
            return self.close()
        if self._handle:
            self.reactor.watch(handle, not self._paused, 0)
