# coding: utf-8

import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

    import Pyjo.DOM

    # Empty
    is_ok(str(Pyjo.DOM.new()), '', 'right result')
    is_ok(str(Pyjo.DOM.new('')), '', 'right result')
    is_ok(str(Pyjo.DOM.new().parse('')), '', 'right result')

    # Simple (basics)
    dom = Pyjo.DOM.new('<div><div FOO="0" id="a">A</div><div id="b">B</div></div>')
    is_ok(dom.at('#b').text, 'B', 'right text')
    div = []
    div.extend(dom.find('div[id]').map('text').each())
    is_deeply_ok(div, ['A', 'B'], 'found all div elements with id')
    div = []
    dom.find('div[id]').each(lambda i, n: div.append(i.text))
    is_deeply_ok(div, ['A', 'B'], 'found all div elements with id')
    is_ok(dom.at('#a').attr('foo'), '0', 'right attribute')
    is_ok(dom.at('#a').attr()['foo'], '0', 'right attribute')
    is_ok(dom, '<div><div foo="0" id="a">A</div><div id="b">B</div></div>', 'right result')

    # Tap into method chain
    dom = Pyjo.DOM.new().parse('<div id="a">A</div><div id="b">B</div>')
    is_deeply_ok(dom.find('[id]').map('attr', 'id').each(), ['a', 'b'], 'right result')
    is_ok(str(dom.tap(lambda i: i.at('#b').remove())), '<div id="a">A</div>', 'right result')

    # Simple nesting with healing (tree structure)
    dom = Pyjo.DOM.new('<foo><bar a="b&lt;c">ju<baz a23>s<bazz />t</bar>works</foo>')
    is_ok(dom.tree[0], 'root', 'right element')
    is_ok(dom.tree[1][0], 'tag', 'right element')
    is_ok(dom.tree[1][1], 'foo', 'right tag')
    is_deeply_ok(dom.tree[1][2], {}, 'empty attributes')
    is_ok(dom.tree[1][3], dom.tree, 'right parent')
    is_ok(dom.tree[1][4][0], 'tag', 'right element')
    is_ok(dom.tree[1][4][1], 'bar', 'right tag')
    is_deeply_ok(dom.tree[1][4][2], {'a': 'b<c'}, 'right attributes')
    is_ok(dom.tree[1][4][3], dom.tree[1], 'right parent')
    is_ok(dom.tree[1][4][4][0], 'text', 'right element')
    is_ok(dom.tree[1][4][4][1], 'ju', 'right text')
    is_ok(dom.tree[1][4][4][2], dom.tree[1][4], 'right parent')
    is_ok(dom.tree[1][4][5][0], 'tag', 'right element')
    is_ok(dom.tree[1][4][5][1], 'baz', 'right tag')
    is_deeply_ok(dom.tree[1][4][5][2], {'a23': None}, 'right attributes')
    is_ok(dom.tree[1][4][5][3], dom.tree[1][4], 'right parent')
    is_ok(dom.tree[1][4][5][4][0], 'text', 'right element')
    is_ok(dom.tree[1][4][5][4][1], 's', 'right text')
    is_ok(dom.tree[1][4][5][4][2], dom.tree[1][4][5], 'right parent')
    is_ok(dom.tree[1][4][5][5][0], 'tag', 'right element')
    is_ok(dom.tree[1][4][5][5][1], 'bazz', 'right tag')
    is_deeply_ok(dom.tree[1][4][5][5][2], {}, 'empty attributes')
    is_ok(dom.tree[1][4][5][5][3], dom.tree[1][4][5], 'right parent')
    is_ok(dom.tree[1][4][5][6][0], 'text', 'right element')
    is_ok(dom.tree[1][4][5][6][1], 't', 'right text')
    is_ok(dom.tree[1][4][5][6][2], dom.tree[1][4][5], 'right parent')
    is_ok(dom.tree[1][5][0], 'text', 'right element')
    is_ok(dom.tree[1][5][1], 'works', 'right text')
    is_ok(dom.tree[1][5][2], dom.tree[1], 'right parent')
    is_ok(dom, '<foo><bar a="b&lt;c">ju<baz a23>s<bazz></bazz>t</baz></bar>works</foo>', 'right result')

    # Select based on parent
    dom = Pyjo.DOM.new("""
    <body>
      <div>test1</div>
      <div><div>test2</div></div>
    <body>
    """)
    is_ok(dom.find('body > div')[0].text, 'test1', 'right text')
    is_ok(dom.find('body > div')[1].text, '', 'no content')
    throws_ok(lambda: dom.find('body > div')[2], IndexError, 'no result')
    is_ok(dom.find('body > div').size, 2, 'right number of elements')
    is_ok(dom.find('body > div > div')[0].text, 'test2', 'right text')
    throws_ok(lambda: dom.find('body > div > div')[1], IndexError, 'no result')
    is_ok(dom.find('body > div > div').size, 1, 'right number of elements')

    # A bit of everything (basic navigation)
    dom = Pyjo.DOM.new().parse("""<!doctype foo>
    <foo bar="ba&lt;z">
      test
      <simple class="working">easy</simple>
      <test foo="bar" id="test" />
      <!-- lala -->
      works well
      <![CDATA[ yada yada]]>
      <?boom lalalala ?>
      <a little bit broken>
      < very broken
      <br />
      more text
    </foo>""")
    ok(not dom.xml, 'XML mode not detected')
    is_ok(dom.type, None, 'no type')
    is_ok(dom.attr('foo'), None, 'no attribute')
    is_ok(dom.attr(foo='bar').attr('foo'), None, 'no attribute')
    is_ok(dom.tree[1][0], 'doctype', 'right element')
    is_ok(dom.tree[1][1], ' foo', 'right doctype')
    is_ok(dom, """<!DOCTYPE foo>
    <foo bar="ba&lt;z">
      test
      <simple class="working">easy</simple>
      <test foo="bar" id="test"></test>
      <!-- lala -->
      works well
      <![CDATA[ yada yada]]>
      <?boom lalalala ?>
      <a bit broken little>
      &lt; very broken
      <br>
      more text
    </a></foo>""", 'right result')
    simple = dom.at('foo simple.working[class^="wor"]')
    is_ok(simple.parent.all_text, 'test easy works well yada yada < very broken more text', 'right text')
    is_ok(simple.type, 'simple', 'right type')
    is_ok(simple.attr('class'), 'working', 'right class attribute')
    is_ok(simple.text, 'easy', 'right text')
    is_ok(simple.parent.type, 'foo', 'right parent type')
    is_ok(simple.parent['bar'], 'ba<z', 'right parent attribute')
    is_ok(simple.parent.children()[1].type, 'test', 'right sibling')
    is_ok(simple.to_str(), '<simple class="working">easy</simple>', 'stringified right')
    simple.parent.attr('bar', 'baz').attr(this='works', too='yea')
    is_ok(simple.parent.attr('bar'), 'baz', 'right parent attribute')
    is_ok(simple.parent.attr('this'), 'works', 'right parent attribute')
    is_ok(simple.parent.attr('too'), 'yea', 'right parent attribute')
    is_ok(dom.at('test#test').type, 'test', 'right type')
    is_ok(dom.at('[class$="ing"]').type, 'simple', 'right type')
    is_ok(dom.at('[class="working"]').type, 'simple', 'right type')
    is_ok(dom.at('[class$=ing]').type, 'simple', 'right type')
    is_ok(dom.at('[class=working][class]').type, 'simple', 'right type')
    is_ok(dom.at('foo > simple').next.type, 'test', 'right type')
    is_ok(dom.at('foo > simple').next.next.type, 'a', 'right type')
    is_ok(dom.at('foo > test').previous.type, 'simple', 'right type')
    is_ok(dom.next, None, 'no siblings')
    is_ok(dom.previous, None, 'no siblings')
    is_ok(dom.at('foo > a').next, None, 'no next sibling')
    is_ok(dom.at('foo > simple').previous, None, 'no previous sibling')
    is_deeply_ok(dom.at('simple').ancestors().map('type').each(), ['foo'], 'right results')
    ok(not dom.at('simple').ancestors().first().xml, 'XML mode not active')

    # Nodes
    dom = Pyjo.DOM.new('<!DOCTYPE before><p>test<![CDATA[123]]><!-- 456 --></p><?after?>')
    is_ok(dom.at('p').preceding_siblings().first().content, ' before', 'right content')
    is_ok(dom.at('p').preceding_siblings().size, 1, 'right number of nodes')
    is_ok(dom.at('p').contents.last().preceding_siblings().first().content, 'test', 'right content')
    is_ok(dom.at('p').contents.last().preceding_siblings().last().content, '123', 'right content')
    is_ok(dom.at('p').contents.last().preceding_siblings().size, 2, 'right number of nodes')
    is_ok(dom.preceding_siblings().size, 0, 'no preceding nodes')
    is_ok(dom.at('p').following_siblings().first().content, 'after', 'right content')
    is_ok(dom.at('p').following_siblings().size, 1, 'right number of nodes')
    is_ok(dom.contents.first().following_siblings().first().type, 'p', 'right type')
    is_ok(dom.contents.first().following_siblings().last().content, 'after', 'right content')
    is_ok(dom.contents.first().following_siblings().size, 2, 'right number of nodes')
    is_ok(dom.following_siblings().size, 0, 'no following nodes')
    is_ok(dom.at('p').previous_sibling.content, ' before', 'right content')
    is_ok(dom.at('p').previous_sibling.previous_sibling, None, 'no more siblings')
    is_ok(dom.at('p').next_sibling.content, 'after', 'right content')
    is_ok(dom.at('p').next_sibling.next_sibling, None, 'no more siblings')
    is_ok(dom.at('p').contents.last().previous_sibling.previous_sibling.content, 'test', 'right content')
    is_ok(dom.at('p').contents.first().next_sibling.next_sibling.content, ' 456 ', 'right content')
    is_ok(dom.all_contents[0].node, 'doctype', 'right node')
    is_ok(dom.all_contents[0].content, ' before', 'right content')
    is_ok(dom.all_contents[0], '<!DOCTYPE before>', 'right content')
    is_ok(dom.all_contents[1].type, 'p', 'right type')
    is_ok(dom.all_contents[2].node, 'text', 'right node')
    is_ok(dom.all_contents[2].content, 'test', 'right content')
    is_ok(dom.all_contents[5].node, 'pi', 'right node')
    is_ok(dom.all_contents[5].content, 'after', 'right content')
    is_ok(dom.at('p').all_contents[0].node, 'text', 'right node')
    is_ok(dom.at('p').all_contents[0].content, 'test', 'right node')
    is_ok(dom.at('p').all_contents.last().node, 'comment', 'right node')
    is_ok(dom.at('p').all_contents.last().content, ' 456 ', 'right node')
    is_ok(dom.contents[1].contents.first().parent.type, 'p', 'right type')
    is_ok(dom.contents[1].contents.first().content, 'test', 'right content')
    is_ok(dom.contents[1].contents.first(), 'test', 'right content')
    is_ok(dom.at('p').contents.first().node, 'text', 'right node')
    is_ok(dom.at('p').contents.first().remove().type, 'p', 'right type')
    is_ok(dom.at('p').contents.first().node, 'cdata', 'right node')
    is_ok(dom.at('p').contents.first().content, '123', 'right content')
    is_ok(dom.at('p').contents[1].node, 'comment', 'right node')
    is_ok(dom.at('p').contents[1].content, ' 456 ', 'right content')
    is_ok(dom.contents[0].node, 'doctype', 'right node')
    is_ok(dom.contents[0].content, ' before', 'right content')
    is_ok(dom.contents[2].node, 'pi', 'right node')
    is_ok(dom.contents[2].content, 'after', 'right content')
    is_ok(dom.contents.first().set(content=' again').content, ' again', 'right content')
    is_ok(dom.contents.grep(lambda i: i.node == 'pi').map('remove').first().node, 'root', 'right node')
    is_ok(dom, '<!DOCTYPE again><p><![CDATA[123]]><!-- 456 --></p>', 'right result')

    # Modify nodes
    dom = Pyjo.DOM.new('<script>la<la>la</script>')
    is_ok(dom.at('script').node, 'tag', 'right node')
    is_ok(dom.at('script').contents[0].node, 'raw', 'right node')
    is_ok(dom.at('script').contents[0].content, 'la<la>la', 'right content')
    is_ok(dom, '<script>la<la>la</script>', 'right result')
    is_ok(dom.at('script').contents.first().replace('a<b>c</b>1<b>d</b>').type, 'script', 'right type')
    is_ok(dom, '<script>a<b>c</b>1<b>d</b></script>', 'right result')
    is_ok(dom.at('b').contents.first().append('e').content, 'c', 'right content')
    is_ok(dom.at('b').contents.first().prepend('f').node, 'text', 'right node')
    is_ok(dom, '<script>a<b>fce</b>1<b>d</b></script>', 'right result')
    is_ok(dom.at('script').contents.first().following().first().type, 'b', 'right type')
    is_ok(dom.at('script').contents.first().next.content, 'fce', 'right content')
    is_ok(dom.at('script').contents.first().previous, None, 'no siblings')
    is_ok(dom.at('script').contents[2].previous.content, 'fce', 'right content')
    is_ok(dom.at('b').contents[1].next, None, 'no siblings')
    is_ok(dom.at('script').contents.first().wrap('<i>:)</i>').root, '<script><i>:)a</i><b>fce</b>1<b>d</b></script>', 'right result')
    is_ok(dom.at('i').contents.first().wrap_content('<b></b>').root, '<script><i><b>:)</b>a</i><b>fce</b>1<b>d</b></script>', 'right result')
    is_ok(dom.at('b').contents.first().ancestors().map('type').join(','), 'b,i,script', 'right result')
    is_ok(dom.at('b').contents.first().append_content('g').content, ':)g', 'right content')
    is_ok(dom.at('b').contents.first().prepend_content('h').content, 'h:)g', 'right content')
    is_ok(dom, '<script><i><b>h:)g</b>a</i><b>fce</b>1<b>d</b></script>', 'right result')
    is_ok(dom.at('script > b:last-of-type').append('<!--y-->').following_siblings().first().content, 'y', 'right content')
    is_ok(dom.at('i').prepend('z').preceding_siblings().first().content, 'z', 'right content')
    is_ok(dom.at('i').following().last().text, 'd', 'right text')
    is_ok(dom.at('i').following().size, 2, 'right number of following elements')
    is_ok(dom.at('i').following('b:last-of-type').first().text, 'd', 'right text')
    is_ok(dom.at('i').following('b:last-of-type').size, 1, 'right number of following elements')
    is_ok(dom.following().size, 0, 'no following elements')
    is_ok(dom.at('script > b:last-of-type').preceding().first().type, 'i', 'right type')
    is_ok(dom.at('script > b:last-of-type').preceding().size, 2, 'right number of preceding elements')
    is_ok(dom.at('script > b:last-of-type').preceding('b').first().type, 'b', 'right type')
    is_ok(dom.at('script > b:last-of-type').preceding('b').size, 1, 'right number of preceding elements')
    is_ok(dom.preceding().size, 0, 'no preceding elements')
    is_ok(dom, '<script>z<i><b>h:)g</b>a</i><b>fce</b>1<b>d</b><!--y--></script>', 'right result')

    # XML nodes
    dom = Pyjo.DOM.new().set(xml=1).parse('<b>test<image /></b>')
    ok(dom.at('b').contents.first().xml, 'XML mode active')
    ok(dom.at('b').contents.first().replace('<br>').contents.first().xml, 'XML mode active')
    is_ok(dom, '<b><br /><image /></b>', 'right result')

    # Treating nodes as elements
    dom = Pyjo.DOM.new('foo<b>bar</b>baz')
    is_ok(dom.contents.first().contents.size, 0, 'no contents')
    is_ok(dom.contents.first().all_contents.size, 0, 'no contents')
    is_ok(dom.contents.first().children().size, 0, 'no children')
    is_ok(dom.contents.first().strip().parent, 'foo<b>bar</b>baz', 'no changes')
    is_ok(dom.contents.first().at('b'), None, 'no result')
    is_ok(dom.contents.first().find('*').size, 0, 'no results')
    is_ok(dom.contents.first().match('*'), None, 'no match')
    is_deeply_ok(dom.contents.first().attr(), {}, 'no attributes')
    is_ok(dom.contents.first().namespace, None, 'no namespace')
    is_ok(dom.contents.first().type, None, 'no type')
    is_ok(dom.contents.first().text, '', 'no text')
    is_ok(dom.contents.first().all_text, '', 'no text')

    # Class and ID
    dom = Pyjo.DOM.new('<div id="id" class="class">a</div>')
    is_ok(dom.at('div#id.class').text, 'a', 'right text')

    # Deep nesting (parent combinator)
    dom = Pyjo.DOM.new("""
    <html>
      <head>
        <title>Foo</title>
      </head>
      <body>
        <div id="container">
          <div id="header">
            <div id="logo">Hello World</div>
            <div id="buttons">
              <p id="foo">Foo</p>
            </div>
          </div>
          <form>
            <div id="buttons">
              <p id="bar">Bar</p>
            </div>
          </form>
          <div id="content">More stuff</div>
        </div>
      </body>
    </html>
    """)
    p = dom.find('body > #container > div p[id]')
    is_ok(p[0].attr('id'), 'foo', 'right id attribute')
    throws_ok(lambda: p[1], IndexError, 'no second result')
    is_ok(p.size, 1, 'right number of elements')
    p = []
    div = []
    dom.find('div').each(lambda i, n: div.append(i.attr('id')))
    dom.find('p').each(lambda i, n: p.append(i.attr('id')))
    is_deeply_ok(p, ['foo', 'bar'], 'found all p elements')
    ids = ['container', 'header', 'logo', 'buttons', 'buttons', 'content']
    is_deeply_ok(div, ids, 'found all div elements')
    is_deeply_ok(dom.at('p').ancestors().map('type').each(),
                 ['div', 'div', 'div', 'body', 'html'], 'right results')
    is_deeply_ok(dom.at('html').ancestors().each(), [], 'no results')
    is_deeply_ok(dom.ancestors().each(), [], 'no results')

    # Script tag
    dom = Pyjo.DOM.new("""
    <script charset="utf-8">alert('lalala')</script>
    """)
    is_ok(dom.at('script').text, "alert('lalala')", 'right script content')

    # HTML5 (unquoted values)
    dom = Pyjo.DOM.new('<div id = test foo ="bar" class=tset bar=/baz/ baz=//>works</div>')
    is_ok(dom.at('#test').text, 'works', 'right text')
    is_ok(dom.at('div').text, 'works', 'right text')
    is_ok(dom.at('[foo=bar][foo="bar"]').text, 'works', 'right text')
    is_ok(dom.at('[foo="ba"]'), None, 'no result')
    is_ok(dom.at('[foo=bar]').text, 'works', 'right text')
    is_ok(dom.at('[foo=ba]'), None, 'no result')
    is_ok(dom.at('.tset').text, 'works', 'right text')
    is_ok(dom.at('[bar=/baz/]').text, 'works', 'right text')
    is_ok(dom.at('[baz=//]').text, 'works', 'right text')

    # HTML1 (single quotes, uppercase tags and whitespace in attributes)
    dom = Pyjo.DOM.new('''<DIV id = 'test' foo ='bar' class= "tset">works</DIV>''')
    is_ok(dom.at('#test').text, 'works', 'right text')
    is_ok(dom.at('div').text, 'works', 'right text')
    is_ok(dom.at('[foo="bar"]').text, 'works', 'right text')
    is_ok(dom.at('[foo="ba"]'), None, 'no result')
    is_ok(dom.at('[foo=bar]').text, 'works', 'right text')
    is_ok(dom.at('[foo=ba]'), None, 'no result')
    is_ok(dom.at('.tset').text, 'works', 'right text')

    # Already decoded Unicode snowman and quotes in selector
    dom = Pyjo.DOM.new(u'<div id="snowm&quot;an">☃</div>')
    is_ok(dom.at(r'[id="snowm\"an"]').text, u'☃', 'right text')
    is_ok(dom.at(r'[id="snowm\22 an"]').text, u'☃', 'right text')
    is_ok(dom.at(r'[id="snowm\000022an"]').text, u'☃', 'right text')
    is_ok(dom.at(r'[id="snowm\22an"]'), None, 'no result')
    is_ok(dom.at(r'[id="snowm\21 an"]'), None, 'no result')
    is_ok(dom.at(r'[id="snowm\000021an"]'), None, 'no result')
    is_ok(dom.at(r'[id="snowm\000021 an"]'), None, 'no result')

    # Unicode and escaped selectors
    html = u'<html><div id="☃x">Snowman</div><div class="x ♥">Heart</div></html>'
    dom = Pyjo.DOM.new(html)
    is_ok(dom.at("#\\\n\\002603x").text, 'Snowman', 'right text')
    is_ok(dom.at('#\\2603 x').text, 'Snowman', 'right text')
    is_ok(dom.at("#\\\n\\2603 x").text, 'Snowman', 'right text')
    is_ok(dom.at('[id="\\\n\\2603 x"]').text, 'Snowman', 'right text')
    is_ok(dom.at('[id="\\\n\\002603x"]').text, 'Snowman', 'right text')
    is_ok(dom.at('[id="\\\\2603 x"]').text, 'Snowman', 'right text')
    is_ok(dom.at("html #\\\n\\002603x").text, 'Snowman', 'right text')
    is_ok(dom.at('html #\\2603 x').text, 'Snowman', 'right text')
    is_ok(dom.at("html #\\\n\\2603 x").text, 'Snowman', 'right text')
    is_ok(dom.at('html [id="\\\n\\2603 x"]').text, 'Snowman', 'right text')
    is_ok(dom.at('html [id="\\\n\\002603x"]').text, 'Snowman', 'right text')
    is_ok(dom.at('html [id="\\\\2603 x"]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'#☃x').text, 'Snowman', 'right text')
    is_ok(dom.at(u'div#☃x').text, 'Snowman', 'right text')
    is_ok(dom.at(u'html div#☃x').text, 'Snowman', 'right text')
    is_ok(dom.at(u'[id^="☃"]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'div[id^="☃"]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'html div[id^="☃"]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'html > div[id^="☃"]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'[id^=☃]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'div[id^=☃]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'html div[id^=☃]').text, 'Snowman', 'right text')
    is_ok(dom.at(u'html > div[id^=☃]').text, 'Snowman', 'right text')
    is_ok(dom.at(".\\\n\\002665").text, 'Heart', 'right text')
    is_ok(dom.at('.\\2665').text, 'Heart', 'right text')
    is_ok(dom.at("html .\\\n\\002665").text, 'Heart', 'right text')
    is_ok(dom.at('html .\\2665').text, 'Heart', 'right text')
    is_ok(dom.at('html [class$="\\\n\\002665"]').text, 'Heart', 'right text')
    is_ok(dom.at('html [class$="\\2665"]').text, 'Heart', 'right text')
    is_ok(dom.at('[class$="\\\n\\002665"]').text, 'Heart', 'right text')
    is_ok(dom.at('[class$="\\2665"]').text, 'Heart', 'right text')
    is_ok(dom.at('.x').text, 'Heart', 'right text')
    is_ok(dom.at('html .x').text, 'Heart', 'right text')
    is_ok(dom.at(u'.♥').text, 'Heart', 'right text')
    is_ok(dom.at(u'html .♥').text, 'Heart', 'right text')
    is_ok(dom.at(u'div.♥').text, 'Heart', 'right text')
    is_ok(dom.at(u'html div.♥').text, 'Heart', 'right text')
    is_ok(dom.at(u'[class$="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'div[class$="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html div[class$="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html > div[class$="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'[class$=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'div[class$=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html div[class$=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html > div[class$=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'[class~="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'div[class~="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html div[class~="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html > div[class~="♥"]').text, 'Heart', 'right text')
    is_ok(dom.at(u'[class~=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'div[class~=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html div[class~=♥]').text, 'Heart', 'right text')
    is_ok(dom.at(u'html > div[class~=♥]').text, 'Heart', 'right text')
    is_ok(dom.at('[class~="x"]').text, 'Heart', 'right text')
    is_ok(dom.at('div[class~="x"]').text, 'Heart', 'right text')
    is_ok(dom.at('html div[class~="x"]').text, 'Heart', 'right text')
    is_ok(dom.at('html > div[class~="x"]').text, 'Heart', 'right text')
    is_ok(dom.at('[class~=x]').text, 'Heart', 'right text')
    is_ok(dom.at('div[class~=x]').text, 'Heart', 'right text')
    is_ok(dom.at('html div[class~=x]').text, 'Heart', 'right text')
    is_ok(dom.at('html > div[class~=x]').text, 'Heart', 'right text')
    is_ok(dom.at('html'), html, 'right result')
    is_ok(dom.at(u'#☃x').parent, html, 'right result')
    is_ok(dom.at(u'#☃x').root, html, 'right result')
    is_ok(dom.children('html').first(), html, 'right result')
    is_ok(dom.to_str(), html, 'right result')
    is_ok(dom.content, html, 'right result')

    # Looks remotely like HTML
    dom = Pyjo.DOM.new(u'<!DOCTYPE H "-/W/D HT 4/E">☃<title class=test>♥</title>☃')
    is_ok(dom.at('title').text, u'♥', 'right text')
    is_ok(dom.at('*').text, u'♥', 'right text')
    is_ok(dom.at('.test').text, u'♥', 'right text')

    # Replace elements
    dom = Pyjo.DOM.new('<div>foo<p>lalala</p>bar</div>')
    is_ok(dom.at('p').replace('<foo>bar</foo>'), '<div>foo<foo>bar</foo>bar</div>', 'right result')
    is_ok(dom, '<div>foo<foo>bar</foo>bar</div>', 'right result')
    #dom.at('foo').replace(Pyjo.DOM.new('text'))
    #is_ok(dom, '<div>footextbar</div>', 'right result')
    dom = Pyjo.DOM.new('<div>foo</div><div>bar</div>')
    dom.find('div').each(lambda i, n: i.replace('<p>test</p>'))
    is_ok(dom, '<p>test</p><p>test</p>', 'right result')
    dom = Pyjo.DOM.new('<div>foo<p>lalala</p>bar</div>')
    is_ok(dom.replace(u'♥'), u'♥', 'right result')
    is_ok(dom, u'♥', 'right result')
    dom.replace('<div>foo<p>lalala</p>bar</div>')
    is_ok(dom, '<div>foo<p>lalala</p>bar</div>', 'right result')
    is_ok(dom.at('p').replace(''), '<div>foobar</div>', 'right result')
    is_ok(dom, '<div>foobar</div>', 'right result')
    is_ok(dom.replace(''), '', 'no result')
    is_ok(dom, '', 'no result')
    dom.replace('<div>foo<p>lalala</p>bar</div>')
    is_ok(dom, '<div>foo<p>lalala</p>bar</div>', 'right result')
    dom.find('p').map('replace', '')
    is_ok(dom, '<div>foobar</div>', 'right result')
    dom = Pyjo.DOM.new(u'<div>♥</div>')
    dom.at('div').set(content=u'☃')
    is_ok(dom, u'<div>☃</div>', 'right result')
    dom = Pyjo.DOM.new(u'<div>♥</div>')
    dom.at('div').set(content=u"\u2603")
    is_ok(dom.to_str(), u'<div>☃</div>', 'right result')
    is_ok(dom.at('div').replace(u'<p>♥</p>').root, u'<p>♥</p>', 'right result')
    is_ok(dom.to_str(), u'<p>♥</p>', 'right result')
    is_ok(dom.replace('<b>whatever</b>').root, '<b>whatever</b>', 'right result')
    is_ok(dom.to_str(), '<b>whatever</b>', 'right result')
    dom.at('b').prepend('<p>foo</p>').append('<p>bar</p>')
    is_ok(dom, '<p>foo</p><b>whatever</b><p>bar</p>', 'right result')
    is_ok(dom.find('p').map('remove').first().root.at('b').text, 'whatever', 'right result')
    is_ok(dom, '<b>whatever</b>', 'right result')
    is_ok(dom.at('b').strip(), 'whatever', 'right result')
    is_ok(dom.strip(), 'whatever', 'right result')
    is_ok(dom.remove(), '', 'right result')
    dom.replace('A<div>B<p>C<b>D<i><u>E</u></i>F</b>G</p><div>H</div></div>I')
    is_ok(dom.find(':not(div):not(i):not(u)').map('strip').first().root, 'A<div>BCD<i><u>E</u></i>FG<div>H</div></div>I', 'right result')
    is_ok(dom.at('i').to_str(), '<i><u>E</u></i>', 'right result')
    dom = Pyjo.DOM.new('<div><div>A</div><div>B</div>C</div>')
    is_ok(dom.at('div').at('div').text, 'A', 'right text')
    dom.at('div').find('div').map('strip')
    is_ok(dom, '<div>ABC</div>', 'right result')

    done_testing()
