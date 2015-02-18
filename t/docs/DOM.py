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

    expected = [None, 'b', 'a']
    dom.find('p[id]').reverse().each(lambda i, num: is_ok(i.attr('id'), expected[num], "elem[{0}].attr()".format(num)))

    expected = [None, 'a:Test', 'b:123']
    num = 1
    for i in dom.find('p[id]').each():
        is_ok(i.attr('id') + ':' + i.text, expected[num], "elem[{0}].attr()".format(num))
        num += 1

    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')
    dom.find('div p').last().append('<p id="c">456</p>')
    is_ok(dom.to_str(), '<div><p id="a">Test</p><p id="b">123</p><p id="c">456</p></div>', "dom.append()")

    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')
    dom.find(':not(p)').map('strip')
    is_ok(dom.to_str(), '<p id="a">Test</p><p id="b">123</p>', "dom.strip()")

    # new
    dom = Pyjo.DOM.new()
    isa_ok(dom, Pyjo.DOM.object, "dom")
    is_ok(dom, '', "dom")

    # html
    isa_ok(dom.html, Pyjo.DOM.HTML.object, "dom.html")
    is_ok(dom.html.render(), "", "dom.html.render()")

    # all_contents
    is_ok(dom.parse('<p><!-- Test --><b>123<!-- 456 --></b></p>')
          .all_contents
          .grep(lambda i: i.node == 'comment').map('remove').first(),
          "<p><b>123</b></p>", 'all_contents result')

    # all_text
    is_ok(dom.parse("<div>foo\n<p>bar</p>baz\n</div>").at('div').all_text,
          "foo bar baz", 'all_text result')

    # all_raw_text
    is_ok(dom.parse("<div>foo\n<p>bar</p>baz\n</div>").at('div').all_raw_text,
          "foo\nbar baz\n", 'all_raw_text result')

    # ancestors
    is_ok(dom.parse("<div><p><i>bar</i></p></div>").at('i').contents[0]
          .ancestors()
          .reverse().map('type').join(" > "),
          "div > p > i", 'ancestors result')

    # append
    is_ok(dom.parse('<div><h1>Test</h1></div>')
          .at('h1').append('<h2>123</h2>').root,
          "<div><h1>Test</h1><h2>123</h2></div>", 'append result')

    is_ok(dom.parse('<p>Test</p>').at('p').contents.first().append(' 123').root,
          "<p>Test 123</p>", 'append result')

    # append_content
    is_ok(dom.parse('<div><h1>Test</h1></div>')
          .at('h1').append_content('123').root,
          "<div><h1>Test123</h1></div>", 'append_content result')

    is_ok(dom.parse('<!-- Test --><br>')
          .contents.first().append_content('123 ').root,
          "<!-- Test 123 --><br>", 'append_content result')

    is_ok(dom.parse('<p>Test</p>').at('p').append_content('<i>123</i>').root,
          "<p>Test<i>123</i></p>", 'append_content result')

    # at
    is_ok(Pyjo.DOM.new('<svg xmlns:svg="http://www.w3.org/2000/svg" width="520" height="350"></svg>')
          .at('[xmlns\:svg]').attr('xmlns:svg'),
          "http://www.w3.org/2000/svg", 'at result')

    # attr
    is_ok(dom.parse('<div id="a">foo</div><p>bar</p><div id="b">baz</div>')
          .find('*').map('attr', 'id').compact().join("\n"),
          "a\nb", 'attr result')

    # children
    is_ok(dom.parse('<b>foo</b><i>bar</i><p>baz</p>').children().first().type,
          "b", 'children result')

    # content
    is_ok(dom.parse('<div><b>Test</b></div>').at('div').content,
          "<b>Test</b>", 'content result')

    is_ok(dom.parse('<div><h1>Test</h1></div>').at('h1').set(content='123').root,
          "<div><h1>123</h1></div>", 'content result')

    is_ok(dom.parse('<p>Test</p>').at('p').set(content='<i>123</i>').root,
          "<p><i>123</i></p>", 'content result')

    is_ok(dom.parse('<div><h1>Test</h1></div>').at('h1').set(content='').root,
          "<div><h1></h1></div>", 'content result')

    is_ok(dom.parse('<!-- Test --><br>').contents.first().content,
          " Test ", 'content result')

    is_ok(dom.parse('<div><!-- Test -->456</div>')
          .at('div').contents.first().set(content=' 123 ').root,
          "<div><!-- 123 -->456</div>", 'content result')

    # contents
    is_ok(dom.parse('<p>Test<b>123</b></p>').at('p').contents.first().remove(),
          "<p><b>123</b></p>", 'contents result')

    is_ok(dom.parse('<!-- Test --><b>123</b>').contents.first(),
          "<!-- Test -->", 'contents result')

    # find
    is_ok(dom.parse('<div id="a"></div><div id="b"></div><div id="c"></div>')
          .find('div')[2].attr('id'),
          "c", 'find result')

    is_deeply_ok(dom.parse('<h1>a</h1><h2>b</h2><h3>c</h3>')
                 .find('h1, h2, h3').map('text').to_list(),
                 ['a', 'b', 'c'], 'find result')

    is_deeply_ok(dom.parse('<div class="foo.bar">baz</div>')
                 .find('div.foo\.bar').map('content').to_list(),
                 ['baz'], 'find result')

    # following
    is_ok(dom.parse('<b>foo</b><i>bar</i><p>baz</p>').at('b')
          .following().map('type').join("\n"),
          "i\np", 'following result')

    # following_siblings
    is_ok(dom.parse('<p>A</p><!-- B -->C')
          .at('p').following_siblings().last().content,
          "C", 'following_siblings')

    # match
    ok(dom.parse('<p class="a">A</p>').at('p').match('.a'), 'match result is True')
    ok(dom.parse('<p class="a">A</p>').at('p').match('p[class]'), 'match result is True')

    ok(not dom.parse('<p class="a">A</p>').at('p').match('.b'), 'match result is False')
    ok(not dom.parse('<p class="a">A</p>').at('p').match('p[id]'), 'match result is False')

    # namespace
    is_ok(dom.parse('<svg xmlns:svg="http://www.w3.org/2000/svg"><svg:circle cx="1" cy="2" r="3"/></svg>')
          .at('svg > svg\:circle').namespace,
          "http://www.w3.org/2000/svg", 'namespace result')

    is_ok(dom.parse('<svg xmlns:svg="http://www.w3.org/2000/svg"><svg:circle cx="1" cy="2" r="3"/></svg>')
          .at('svg > circle').namespace,
          "http://www.w3.org/2000/svg", 'namespace result')

    # next
    is_ok(dom.parse('<div><h1>Test</h1><h2>123</h2></div>').at('h1').next,
          "<h2>123</h2>", 'next result')

    # next_sibling
    is_ok(dom.parse('<p><b>123</b><!-- Test -->456</p>')
          .at('b').next_sibling.next_sibling,
          "456", 'next_sibling')

    is_ok(dom.parse('<p><b>123</b><!-- Test -->456</p>')
          .at('b').next_sibling.content,
          " Test ", 'next_sibling')

    # preceding
    is_ok(dom.parse('<b>foo</b><i>bar</i><p>baz</p>').at('p')
          .preceding().map('type').join("\n"),
          "b\ni", 'preceding result')

    # preceding_siblings
    is_ok(dom.parse('A<!-- B --><p>C</p>')
          .at('p').preceding_siblings().first().content,
          "A", 'preceding_siblings')

    # prepend
    is_ok(dom.parse('<div><h2>Test</h2></div>')
          .at('h2').prepend('<h1>123</h1>').root,
          "<div><h1>123</h1><h2>Test</h2></div>", 'prepend result')

    is_ok(dom.parse('<p>123</p>').at('p').contents.first().prepend('Test ').root,
          "<p>Test 123</p>", 'prepend result')

    # prepend_content
    is_ok(dom.parse('<div><h2>123</h2></div>')
          .at('h2').prepend_content('Test ').root,
          "<div><h2>Test 123</h2></div>", 'prepend_content result')

    is_ok(dom.parse('<!-- 123 --><br>')
          .contents.first().prepend_content(' Test').root,
          "<!-- Test 123 --><br>", 'prepend_content result')

    is_ok(dom.parse('<p>Test</p>').at('p').prepend_content('<i>123</i>').root,
          "<p><i>123</i>Test</p>", 'prepend_content result')

    # previous
    is_ok(dom.parse('<div><h1>Test</h1><h2>123</h2></div>').at('h2').previous,
          "<h1>Test</h1>", 'previous result')

    # previous_sibling
    is_ok(dom.parse('<p>123<!-- Test --><b>456</b></p>')
          .at('b').previous_sibling.previous_sibling,
          "123", 'previous_sibling result')

    is_ok(dom.parse('<p>123<!-- Test --><b>456</b></p>')
          .at('b').previous_sibling.content,
          " Test ", 'previous_sibling result')

    # raw_text
    is_ok(dom.parse("<div>foo\n<p>bar</p>baz\n</div>").at('div').raw_text,
          "foo\nbaz\n", 'raw_text')

    # remove
    is_ok(dom.parse('<div><h1>Test</h1></div>').at('h1').remove(),
          "<div></div>", 'remove result')

    is_ok(dom.parse('<p>123<b>456</b></p>').at('p').contents.first().remove().root,
          "<p><b>456</b></p>", 'remove result')

    # replace
    is_ok(dom.parse('<div><h1>Test</h1></div>').at('h1').replace('<h2>123</h2>'),
          "<div><h2>123</h2></div>", 'replace result')

    is_ok(dom.parse('<p>Test</p>')
          .at('p').contents.item(0).replace('<b>123</b>').root,
          "<p><b>123</b></p>", 'replace result')

    # strip
    is_ok(dom.parse('<div><h1>Test</h1></div>').at('h1').strip(),
          "<div>Test</div>", 'strip result')

    # text
    is_ok(dom.parse("<div>foo\n<p>bar</p>baz\n</div>").at('div').text,
          "foo baz", 'text result')

    # type
    is_ok(dom.parse('<b>foo</b><i>bar</i><p>baz</p>').children().map('type').join(","),
          "b,i,p", 'type result')

    # wrap
    is_ok(dom.parse('<b>Test</b>').at('b').wrap('<p>123</p>').root,
          "<p>123<b>Test</b></p>", 'wrap result')

    is_ok(dom.parse('<b>Test</b>').at('b').wrap('<div><p></p>123</div>').root,
          "<div><p><b>Test</b></p>123</div>", 'wrap result')

    is_ok(dom.parse('<b>Test</b>').at('b').wrap('<p></p><p>123</p>').root,
          "<p><b>Test</b></p><p>123</p>", 'wrap result')

    is_ok(dom.parse('<p>Test</p>').at('p').contents.first().wrap('<b>').root,
          "<p><b>Test</b></p>", 'wrap result')

    # wrap_content
    is_ok(dom.parse('<p>Test</p>').at('p').wrap_content('<b>123</b>').root,
          "<p><b>123Test</b></p>", 'wrap_content result')

    is_ok(dom.parse('<b>Test</b>').wrap_content('<p></p><p>123</p>'),
          "<p><b>Test</b></p><p>123</p>", 'wrap_content result')

    done_testing()
