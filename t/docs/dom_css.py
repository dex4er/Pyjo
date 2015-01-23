# -*- coding: utf-8 -*-

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.DOM.CSS

    html = Pyjo.DOM.HTML.new().parse('<h1>1</h1><h2>2</h2><h3>3</h3>')
    css = Pyjo.DOM.CSS.new(tree=html.tree)
    isa_ok(css, Pyjo.DOM.CSS.object, "css")
    tree = css.tree
    is_ok(tree[0], 'root', "tree")
    elements = css.select('h1, h2, h3')
    isa_ok(elements, list, 'elements')
    is_ok(len(elements), 3, 'len(elements)')

    done_testing()
