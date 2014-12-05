from __future__ import print_function

import Pyjo.Base

from Pyjo.Util import has


@has(['x', 'y'], 0)
class Point(Pyjo.Base.object):
    pass


@has(['p1', 'p2'], lambda: Point())
class Line(Pyjo.Base.object):
    pass


p = Point(x=1, y=2)

line = Line(p1=p)

print("[{0},{1}]".format(line.p1.x, line.p1.y))
print("[{0},{1}]".format(line.p2.x, line.p2.y))
