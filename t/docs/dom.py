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
    is_ok(dom.find('p').map('text').join("\n"), "Test\n123", "dom.find()")
    is_ok(dom.find('[id]').map('attr', 'id').join("\n"), "a\nb", "dom.find()")

    expected = [None, 'a', 'b']
    dom.find('p[id]').reverse().each(lambda i, num: is_ok(i.attr('id'), expected[num], "elem[{0}].attr()".format(num)))

    expected = [None, 'a:Test', 'b:123']
    num = 1
    for i in dom.find('p[id]').each():
        is_ok(i.attr('id') + ':' + i.text, expected[num], "elem[{0}].attr()".format(num))
        num += 1

    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')
    dom.find('div p').last().append('<p id="c">456</p>')
    is_ok(dom.to_str(), '<div><p id="a">Test</p><p id="b">123</p><p id="c">456</p></div>', "dom.")

    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')
    #dom.find(':not(p)').map('strip')
    #is_ok(dom.to_str(), '', "dom.")

    done_testing()
