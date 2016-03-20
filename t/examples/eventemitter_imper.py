import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # noqa

    import Pyjo.EventEmitter

    plan_tests(5)

    class Cat(Pyjo.EventEmitter.object):
        def poke(self, times):
            self.emit('roar', times)

        def kill(self):
            self.emit('dead')

    def roar_cb(cat, times):
        for _ in range(0, times):
            pass_ok('RAWR!')

    def dead_cb(cat):
        pass_ok('(x.x)')

    tiger = Cat()

    tiger.on(roar_cb, 'roar')
    tiger.once(dead_cb, 'dead')

    tiger.poke(2)
    tiger.poke(2)
    tiger.kill()
    tiger.kill()

    done_testing()
