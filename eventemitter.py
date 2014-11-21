from __future__ import print_function

import Pyjo.EventEmitter


class Cat(Pyjo.EventEmitter.object):
    def poke(self):
        self.emit('roar', 3)


def roar(name, times):
    for _ in range(0, times):
        print('RAWR!')


tiger = Cat()
tiger.on('roar', roar)
tiger.poke()
