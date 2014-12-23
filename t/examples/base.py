import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

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

    is_ok("[{0},{1}]".format(line.p1.x, line.p1.y), "[1,2]", 'line.p1')
    is_ok("[{0},{1}]".format(line.p2.x, line.p2.y), "[0,0]", 'line.p2')

    done_testing()
