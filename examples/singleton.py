from __future__ import print_function

import Pyjo.IOLoop
from Pyjo.IOLoop import Pyjo_IOLoop

print(Pyjo.IOLoop.singleton)
print(Pyjo_IOLoop.singleton)
print(Pyjo_IOLoop().singleton)
