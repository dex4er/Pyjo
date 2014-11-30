import os
import subprocess
import sys
import unittest


class Test(unittest.TestCase):
    def test_pyjo_eventemitter(self):
        os.putenv('PYTHONPATH', '.')
        subprocess.check_output([sys.executable, __file__])


if __name__ == '__main__':

    from Pyjo.Test import *

    from Pyjo.EventEmitter import *

    # Normal event
    e = Pyjo_EventEmitter()
    called = 0
    def cb(self):
        global called
        called += 1
    e.on('test1', cb)
    e.emit('test1')
    is_ok(called, 1, 'event was emitted once')

    # Error
    def cb(self):
        raise Exception('works!')
    e.on('die', cb)
    error = ''
    try:
        e.emit('die')
    except Exception as ex:
        error = str(ex)
    is_ok(error, "works!", 'right error')

    done_testing()
