from __future__ import print_function

import Pyjo.Base

from Pyjo.Util import lazy


class Point(Pyjo.Base.object):
    x = 0
    y = 0


class Line(Pyjo.Base.object):
    p1 = lazy(lambda self: Point())
    p2 = lazy(lambda self: Point())


p = Point(x=1, y=2)

line = Line(p1=p)

print("[{0},{1}]".format(line.p1.x, line.p1.y))
print("[{0},{1}]".format(line.p2.x, line.p2.y))
