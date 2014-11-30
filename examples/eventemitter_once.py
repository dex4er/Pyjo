from __future__ import print_function

from Pyjo.EventEmitter import *


class Cat(Pyjo_EventEmitter):
    def poke(self, times):
        self.emit('roar', times)


def roar_cb(cat, times):
    for _ in range(0, times):
        print('RAWR!')


tiger = Cat()

tiger.once('roar', roar_cb)

tiger.poke(2)
tiger.poke(2)
