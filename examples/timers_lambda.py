from __future__ import print_function

import Pyjo.IOLoop


writer = Pyjo.IOLoop.recurring(0, lambda loop: print("A"))
Pyjo.IOLoop.timer(1, lambda loop: loop.remove(writer))

Pyjo.IOLoop.start()
