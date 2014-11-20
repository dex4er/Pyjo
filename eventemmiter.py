import Pyjo.EventEmmiter


class Cat(Pyjo.EventEmmiter.object):
    def poke(self):
        self.emit('roar', 3)


def roar(name, times):
    for _ in range(0, times):
        print 'RAWR!'


tiger = Cat()
tiger.on('roar', roar)
tiger.poke()
