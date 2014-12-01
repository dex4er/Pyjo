import Pyjo.Test

class Test_Pyjo_EventEmitter(Pyjo.Test.TestCase):
    def test_run(self):
        super(Test_Pyjo_EventEmitter, self).test_run(__file__)


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
