from __future__ import print_function

import Pyjo.EventEmitter

from Pyjo.EventEmitter import on, once


class Cat(Pyjo.EventEmitter.object):
    def poke(self, times):
        self.emit('roar', times)

    def kill(self):
        self.emit('dead')


tiger = Cat()


@on(tiger, 'roar')
def roar_cb(cat, times):
    for _ in range(0, times):
        print('RAWR!')


@once(tiger, 'dead')
def dead_cb(cat):
    print('(x.x)')


tiger.poke(2)
tiger.poke(2)
tiger.kill()
tiger.kill()
