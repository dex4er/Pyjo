from __future__ import print_function

from Pyjo.Collection import c

import Pyjo.EventEmitter
import sys


n = int(c(sys.argv).get(1) or 1000000)


class EV(Pyjo.EventEmitter.object):
    pass


ev = EV()


@ev.on
def event(ev):
    pass


for i in range(n):
    ev.emit('event')
