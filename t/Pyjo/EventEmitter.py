import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':
    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.EventEmitter

    # Normal event
    e = Pyjo.EventEmitter.object()
    called1 = 0

    @e.on
    def test1(self):
        global called1
        called1 += 1

    e.emit('test1')
    is_ok(called1, 1, 'event test1 was emitted, called1')

    # Imperative syntax
    called2 = 0

    def cb(self):
        global called2
        called2 += 1

    e.on(cb, 'test2')
    e.emit('test2')
    is_ok(called2, 1, 'event test2 was emitted, called2')

    # Error
    @e.on
    def die(self):
        raise Exception('works!')
    error = ''
    try:
        e.emit('die')
    except Exception as ex:
        error = str(ex)
    is_ok(error, "works!", 'right error')

    done_testing()
