# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.DOM

    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')
    isa_ok(dom, Pyjo.DOM.object, "dom")

    is_ok(dom.at('#b').text, '123', "dom.at()")
    is_ok(dom.find('p').map('text').join("\n"),  "Test\n123", "dom.find()")

    done_testing()
