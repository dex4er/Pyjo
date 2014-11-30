import os
import subprocess
import unittest


class Test(unittest.TestCase):
    def test_pyjo_eventemitter(self):
        os.putenv('PYTHONPATH', '.')
        subprocess.check_output(['python', __file__])


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
    err = ''
    try:
        e.emit('die')
    except Exception as err:
        err = str(err)
    is_ok(err, "works!", 'right error')

    done_testing()
