# -*- coding: utf-8 -*-

"""
Pyjo.Log - Simple logger
========================
::

    import Pyjo.Log

    # Log to STDERR
    log = Pyjo.Log.new()

    # Customize log file location and minimum log level
    log = Pyjo.Log.new(path='/var/log/pyjo.log', level='warn')

    # Log messages
    log.debug('Not sure what is happening here')
    log.info('FYI: it happened again')
    log.warn('This might be a problem')
    log.error('Garden variety error')
    log.fatal('Boom')

:mod:`Pyjo.Log` is a simple logger for :mod:`Pyjo` projects.

Events
------

:mod:`Pyjo.Log` inherits all events from :mod:`Pyjo.EventEmitter` and can emit the
following new ones.

message
~~~~~~~
::

    @log.on
    def message(log, level, *lines):
       ...

Emitted when a new message gets logged. ::

    log.unsubscribe('message')

    @log.on
    def message(log, level, *lines):
        print("{0}: {1}".format(level, "\n".join(lines))

Classes
-------
"""

import Pyjo.EventEmitter

from Pyjo.Base import lazy


class Pyjo_Log(Pyjo.EventEmitter.object):
    """
    :mod:`Pyjo.Log` inherits all attributes and methods from
    :mod:`Pyjo.EventEmitter` and implements the following new ones.
    """


new = Pyjo_Log.new
object = Pyjo_Log  # @ReservedAssignment
