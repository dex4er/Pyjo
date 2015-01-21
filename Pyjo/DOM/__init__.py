# -*- coding: utf-8 -*-

"""
Pyjo.DOM - Minimalistic HTML/XML DOM parser with CSS selectors
==============================================================
::

    import Pyjo.DOM

    # Parse
    dom = Pyjo.DOM.new('<div><p id="a">Test</p><p id="b">123</p></div>')

    # Find
    dom.at('#b').text().say()
    print(dom.find('p').map('text').join("\\n"))
    dom.find('[id]').map(attr='id').join("\\n")

    # Iterate
    dom.find('p[id]').reverse().each(lambda e: print(e.id))

    # Loop
    for e in dom.find('p[id]').each():
        print(e.id + ':' + e.text())

    # Modify
    dom.find('div p').last().append('<p id="c">456</p>')
    dom.find(':not(p)').map('strip')

    # Render
    print(dom)

:mod:`Pyjo.DOM` is a minimalistic and relaxed HTML/XML DOM parser with CSS
selector support. It will even try to interpret broken HTML and XML, so you
should not use it for validation.
"""


import Pyjo.Base
import Pyjo.Collection
import Pyjo.DOM.CSS
import Pyjo.DOM.HTML
import Pyjo.Mixin.String
import Pyjo.TextStream

from Pyjo.Base import lazy
from Pyjo.Regexp import m, s
from Pyjo.Util import squish, u


class Pyjo_DOM(Pyjo.Base.object, Pyjo.Mixin.String.object):
    """::

        dom = Pyjo.DOM.new()

    Construct a new :mod:`Pyjo.DOM` object.
    """

    html = lazy(lambda self: Pyjo.DOM.HTML.new())

    def __init__(self, html=None):
        if html is not None:
            self.parse(html)

    def __getitem__(self, key):
        return self.attr(key)

    def __setitem__(self, key, value):
        return self.attr(key, value)

    def __delitem__(self, key):
        del self.attr()[key]

    @property
    def all_contents(self):
        """::

            collection = dom.all_contents

        Return a :mod:`Pyjo.Collection` object containing all nodes in DOM structure as
        :mod:`Pyjo.DOM` objects. ::

            # "<p><b>123</b></p>"
            dom.parse('<p><!-- Test --><b>123<!-- 456 --></b></p>')
               .all_contents
               .grep(lambda i: i.node == 'comment').map('remove').first()
        """
        return self._collect(self._all(self._nodes(self.tree)))

    @property
    def all_text(self, trim=True):
        """::

            trimmed   = dom.all_text

        Extract all text content from DOM structure, smart whitespace trimming is
        enabled. ::

            # "foo bar baz"
            dom.parse("<div>foo\\n<p>bar</p>baz\\n</div>").at('div').all_text
        """
        return self._all_text(True, True)

    @property
    def all_raw_text(self, trim=True):
        """::

            untrimmed = dom.all_raw_text

        Extract all text content from DOM structure, smart whitespace trimming is
        disabled. ::

            # "foo\\nbar baz\\n"
            dom.parse("<div>foo\\n<p>bar</p>baz\\n</div>").at('div').all_raw_text
        """
        return self._all_text(True, trim)

    @property
    def ancestors(self):
        """::

            collection = dom.ancestors

        Find all ancestors of this node and return a
        :mod:`Pyjo.Collection` object containing these elements as :mod:`Pyjo.DOM` objects.
        """
        return self._collect(self._ancestors())

    def at(self, pattern):
        """::

            result = dom.at('div > p')

        Find first element in DOM structure matching the CSS selector and return it as
        a :mod:`Pyjo.DOM` object or return :class:`None` if none could be found. All selectors
        from :mod:`Pyjo.DOM.CSS` are supported. ::

            # Find first element with ``svg`` namespace definition
            namespace = dom.at('[xmlns\:svg]')['xmlns:svg']
        """
        result = self._css.select_one(pattern)
        if result:
            return self._build(result, self.xml)

    def attr(self, *args, **kwargs):
        """::

            my_dict = dom.attr()
            foo = dom.attr('foo')
            dom = dom.attr('foo', 'bar')
            dom = dom.attr(foo='bar')

        This element's attributes. Returns :class:`None` if attribute is missing.
        Setting value to :class:`None` deletes attribute. ::

            # List id attributes
            dom.find('*').map('attr', 'id').compact().join("\n").say()
        """
        tree = self.tree

        if tree[0] != 'tag':
            attrs = {}
        else:
            attrs = tree[2]

        # Dict
        if not args and not kwargs:
            return attrs

        # Get
        if len(args) == 1:
            attrs = self.to_dict()
            if args[0] in attrs:
                return attrs[args[0]]
            else:
                return

        # Set
        if len(args) == 2:
            attrs[args[0]] = args[1]

        for k, v in kwargs.items():
            if v is None:
                if k in attrs:
                    del attrs[k]
            else:
                attrs[k] = u(v)

        return self

    @property
    def children(self):
        """::

            collection = dom.children

        Find all children of this element and return a
        :mod:`Pyjo.Collection` object containing these elements as :mod:`Pyjo.DOM` objects. ::

            # Show type of random child element
            print(dom.children.shuffle().first().type)
        """
        return self._collect(self._nodes(self.tree, True))

    @property
    def contents(self):
        """::

            collection = dom.contents

        Return a :mod:`Pyjo.Collection` object containing the child nodes of this element
        as :mod:`Pyjo.DOM` objects. ::

            # "<p><b>123</b></p>"
            dom.parse('<p>Test<b>123</b></p>').at('p').contents.first().remove()

            # "<!-- Test -->"
            dom.parse('<!-- Test --><b>123</b>').contents.first()
        """
        return self._collect(self._nodes(self.tree))

    def find(self, pattern):
        """::

            collection = dom.find('div > p')

        Find all elements in DOM structure matching the CSS selector and return a
        :mod:`Pyjo.Collection` object containing these elements as :mod:`Pyjo.DOM` objects.
        All selectors from :mod:`Pyjo.DOM.CSS` are supported. ::

            # Find a specific element and extract information
            div_id = dom.find('div')[23]['id']

            # Extract information from multiple elements
            headers = dom.find('h1, h2, h3').map('text').to_list()

            # Find elements with a class that contains dots
            divs = dom.find('div.foo\.bar').to_list()
        """
        return self._collect(self._css.select(pattern))

    @property
    def next(self):
        """::

            sibling = dom.next

        Return :mod:`Pyjo.DOM` object for next sibling element or :class:`None` if there are
        no more siblings. ::

            # "<h2>123</h2>"
            dom.parse('<div><h1>Test</h1><h2>123</h2></div>').at('h1').next
        """
        return self._maybe(self._siblings(True, 0)[1])

    @property
    def next_sibling(self):
        """::

            sibling = dom.next_sibling

        Return :mod:`Pyjo.DOM` object for next sibling node or :class:`None` if there are
        no more siblings. ::

            # "456"
            dom.parse('<p><b>123</b><!-- Test -->456</p>')
               .at('b').next_sibling.next_sibling

            # " Test "
            dom.parse('<p><b>123</b><!-- Test -->456</p>')
               .at('b').next_sibling.content
        """
        return self._maybe(self._siblings(False, 0)[1])

    @property
    def node(self):
        """::

            nodetype = dom.node

        This node's type, usually ``cdata``, ``comment``, ``doctype``, ``pi``, ``raw``,
        ``root``, ``tag`` or ``text``.
        """
        return self.tree[0]

    @property
    def parent(self):
        """::

            parent = dom.parent

        Return :mod:`Pyjo.DOM` object for parent of this node or :obj:`None` if this node
        has no parent.
        """
        if self.tree[0] == 'root':
            return
        else:
            return self._build(self._parent(), self.xml)

    def parse(self, html):
        """::

            dom = dom.parse(u'<foo bar="baz">I ♥ Mojolicious!</foo>')

        Parse HTML/XML fragment with :mod:`Pyjo.DOM.HTML`. ::

            # Parse XML
            dom = Pyjo.DOM.new().set(xml=True).parse(xml)
        """
        self.html.parse(html)
        return self

    @property
    def preceding(self):
        return self._collect(self._siblings(True)[0])

    @property
    def preceding_siblings(self):
        """::
            collection = dom.preceding

        Find all sibling elements before this node and
        return a :mod:`Pyjo.Collection` object containing these elements as :mod:`Pyjo.DOM`
        objects.

            # List types of sibling elements before this node
            dom.preceding.map('type').join("\n").say()
        """
        return self._collect(self._siblings(False)[0])

    @property
    def previous(self):
        """::

            sibling = dom.previous

        Return :mod:`Pyjo.DOM` object for previous sibling element or :class:`None` if there
        are no more siblings. ::

            # "<h1>Test</h1>"
            dom.parse('<div><h1>Test</h1><h2>123</h2></div>').at('h2').previous
        """
        return self._maybe(self._siblings(True, -1)[0])

    @property
    def previous_sibling(self):
        """::

            sibling = dom.previous_sibling

        Return :mod:`Pyjo.DOM` object for previous sibling node or :class:`None` if there
        are no more siblings. ::

            # "123"
            dom.parse('<p>123<!-- Test --><b>456</b></p>')
               .at('b').previous_sibling.previous_sibling

            # " Test "
            dom.parse('<p>123<!-- Test --><b>456</b></p>')
               .at('b').previous_sibling.content
        """
        return self._maybe(self._siblings(False, -1)[0])

    @property
    def raw_text(self):
        """::

            untrimmed = dom.raw_text

        Extract text content from this element only (not including child elements),
        smart whitespace trimming is disabled. ::

            # "foo\\nbaz\\n"
            dom.parse("<div>foo\\n<p>bar</p>baz\\n</div>").at('div').raw_text
        """
        return self._all_text(False, False)

    def remove(self):
        """::

            parent = dom.remove()

        Remove this node and return :meth:`parent`. ::

            # "<div></div>"
            dom.parse('<div><h1>Test</h1></div>').at('h1').remove()

            # "<p><b>456</b></p>"
            dom.parse('<p>123<b>456</b></p>').at('p').contents().first().remove().root()
        """
        return self.replace('')

    def replace(self, new):
        """::

            parent = dom.replace(u'<div>I ♥ Mojolicious!</div>')

        Replace this node with HTML/XML fragment and return :meth:`parent`. ::

            # "<div><h2>123</h2></div>"
            dom.parse('<div><h1>Test</h1></div>').at('h1').replace('<h2>123</h2>')

            # "<p><b>123</b></p>"
            dom.parse('<p>Test</p>')
               .at('p').contents().item(0).replace('<b>123</b>').root()
        """
        tree = self.tree
        if tree[0] == 'root':
            return self.parse(new)
        else:
            return self._replace(self._parent(), tree, self._parse(new))

    @property
    def root(self):
        """::

            root = dom.root

        Return :mod:`Pyjo.DOM` object for root node.
        """
        tree = self._ancestors(True)
        if not tree:
            return self
        else:
            return self._build(next(tree), self.xml)

    def to_dict(self):
        return self.attr()

    def to_str(self):
        return self.html.render()

    @property
    def text(self):
        """::

            trimmed = dom.text

        Extract text content from this element only (not including child elements),
        smart whitespace trimming is enabled. ::

            # "foo baz"
            dom.parse("<div>foo\\n<p>bar</p>baz\\n</div>").at('div').text
        """
        return self._all_text(False, True)

    @property
    def tree(self):
        return self.html.tree

    @tree.setter
    def tree(self, value):
        self.html.tree = value

    @property
    def type(self):
        """::

            elemtype = dom.type
            dom.type = 'div'

        This element's type.

            # List types of child elements
            dom.children().map('type').join("\\n").say()
        """
        tree = self.tree
        if tree[0] != 'tag':
            return
        else:
            return tree[1]

    @type.setter
    def type(self, value):
        tree = self.tree
        if tree[0] == 'tag':
            tree[1] = value

    @property
    def xml(self):
        return self.html.xml

    @xml.setter
    def xml(self, value):
        self.html.xml = value

    def _all(self, nodes):
        for n in nodes:
            if n[0] == 'tag':
                yield n
                for a in self._all(self._nodes(n)):
                    yield a
            else:
                yield n

    def _all_text(self, recurse, trim):
        # Detect "pre" tag
        tree = self.tree
        if trim:
            for i in self._ancestors(), (tree,):
                for n in i:
                    if n[1] == 'pre':
                        trim = False

        return self._text(self._nodes(tree), recurse, trim)

    def _ancestors(self, isroot=False):
        if self.node == 'root':
            return

        ancestors = []
        tree = self._parent()

        while True:
            ancestors.append(tree)
            if tree[0] != 'tag':
                break
            tree = tree[3]

        if isroot:
            yield ancestors[-1]
        else:
            for i in ancestors[:-1]:
                yield i

    def _build(self, tree, xml):
        return self.new().set(tree=tree, xml=xml)

    def _collect(self, results):
        xml = self.xml
        return Pyjo.Collection.new(map(lambda a: self._build(a, xml), results))

    @property
    def _css(self):
        return Pyjo.DOM.CSS.new(tree=self.tree)

    def _link(self, children, parent):
        # Link parent to children
        for n in children[1:]:
            yield n
            if n[0] == 'tag':
                offset = 3
            else:
                offset = 2
            n[offset] = parent
            # TODO weakref n[offset]

    def _maybe(self, tree):
        if tree:
            return self._build(tree, self.xml)
        else:
            return None

    def _nodes(self, tree=None, tags=False):
        if not tree:
            return []
        nodes = tree[self._start(tree):]
        if tags:
            return filter(lambda n: n[0] == 'tag', nodes)
        else:
            return nodes

    def _offset(self, parent, child):
        i = self._start(parent)
        for n in parent[i:]:
            if n == child:
                break
            else:
                i += 1
        return i

    def _parent(self):
        return self.tree[3 if self.node == 'tag' else 2]

    def _parse(self, new):
        return Pyjo.DOM.HTML.new(xml=self.xml).parse(new).tree

    def _replace(self, parent, tree, new):
        # splice @$parent, _offset($parent, $tree), 1, _link($new, $parent);
        offset = self._offset(parent, tree)
        parent.pop(offset)
        for n in self._link(new, parent):
            parent.insert(offset, n)
            offset += 1
        return self.parent

    def _select(self, collection, selector=None):
        if selector is None:
            return collection
        else:
            collection.new(filter(lambda i: i.match(selector), collection))

    def _siblings(self, tags, i=None):
        parent = self.parent
        if parent is None:
            return [None, None]

        tree = self.tree
        before = []
        after = []
        match = 0
        for node in self._nodes(parent.tree):
            if not match and node == tree:
                match += 1
                continue
            if tags and node[0] != 'tag':
                continue
            if match:
                after.append(node)
            else:
                before.append(node)

        if i is not None:
            if i >= 0:
                return [before[i] if len(before) > i else None, after[i] if len(after) > i else None]
            else:
                return [before[i] if len(before) >= -i else None, after[i] if len(after) >= -i else None]
        else:
            return [before, after]

    def _start(self, tree):
        if tree[0] == 'root':
            return 1
        else:
            return 4

    def _text(self, nodes, recurse, trim):
        # Merge successive text nodes
        i = 0
        while len(nodes) > i + 1:
            nextnode = nodes[i + 1]
            if nodes[i][0] == 'text' and nextnode[0] == 'text':
                text = nodes[i][1] + nextnode[1]
                nodes.pop(i)
                nodes.pop(i)
                nodes.insert(i, ['text', text])
            else:
                i += 1
                continue

        text = ''
        for node in nodes:
            nodetype = node[0]

            # Text
            chunk = ''
            if nodetype == 'text':
                if trim:
                    chunk = squish(node[1])
                else:
                    chunk = node[1]

            # CDATA or raw text
            elif nodetype == 'cdata' or nodetype == 'raw':
                chunk = node[1]

            # Nested tag
            elif nodetype == 'tag' and recurse:
                chunk = self._text(self._nodes(node), True, False if node[1] == 'pre' else trim)

            # Add leading whitespace if punctuation allows it
            if text == m(r'\S\Z') and chunk == m(r'^[^.!?,;:\s]+'):
                chunk = " " + chunk

            # Trim whitespace blocks
            if chunk == m(r'\S+') or not trim:
                text += chunk

        return text


new = Pyjo_DOM.new
object = Pyjo_DOM  # @ReservedAssignment
