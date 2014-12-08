from __future__ import print_function

import Pyjo.EventEmitter


class Cat(Pyjo.EventEmitter.object):
    def poke(self, times):
        self.emit('roar', times)

    def kill(self):
        self.emit('dead')


tiger = Cat()


@tiger.on('roar')
def cb(cat, times):
    for _ in range(0, times):
        print('RAWR!')


@tiger.once('dead')
def cb(cat):
    print('(x.x)')


tiger.poke(2)
tiger.poke(2)
tiger.kill()
tiger.kill()
