# -*- coding: utf-8 -*-

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

    class Cat(Pyjo.Base.object):
        name = 'Nyan'
        birds = 2
        mice = 2

    class Tiger(Cat):
        friend = lazy(lambda self: Cat())
        stripes = 42

    mew = Cat.new(name='Longcat')
    is_ok(mew.mice, 2, "mew.mice")
    is_ok(mew.set(mice=3, birds=4).mice, 3, "mew.set(...).mice")

    rawr = Tiger.new(stripes=23, mice=0)
    is_ok(rawr.tap(lambda rawr: rawr.friend.set(name='Tacgnol')).mice, 0, "rawr.tap(...).mice")

    done_testing()
