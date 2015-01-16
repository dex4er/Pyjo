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


class Pyjo_DOM(Pyjo.Base.object, Pyjo.Mixin.String.object):
    """::

        dom = Pyjo.DOM.new()

    Construct a new :mod:`Pyjo.DOM` object.
    """

    html = lazy(lambda self: Pyjo.DOM.HTML.new())

    def __init__(self, html=None):
        if html is not None:
            self.parse(html)

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

    def find(self, pattern):
        """::

            collection = dom.find('div > p')

        Find all elements in DOM structure matching the CSS selector and return a
        :mod:`Pyjo.Collection` object containing these elements as :mod:`Pyjo.DOM` objects.
        All selectors from :mod:`Pyjo.DOM.CSS` are supported. ::

            # Find a specific element and extract information
            _id = dom.find('div')[23]['id']

            # Extract information from multiple elements
            headers = dom.find('h1, h2, h3').map('text').each()

            # Find elements with a class that contains dots
            divs = dom.find('div.foo\.bar').each()
        """
        return self._collect(self._css.select(pattern))

    def parse(self, html):
        self.html.parse(html)
        return self

    def to_str(self):
        return self.html.render()

    @property
    def tree(self):
        return self.html.tree

    @tree.setter
    def tree(self, value):
        self.html.tree = value

    @property
    def xml(self):
        return self.html.xml

    @xml.setter
    def xml(self, value):
        self.html.xml = value

    def _build(self, tree, xml):
        return self.new().set(tree=tree, xml=xml)

    def _collect(self, results):
        xml = self.xml
        return Pyjo.Collection.new(map(lambda a: self._build(a, xml), results))

    @property
    def _css(self):
        return Pyjo.DOM.CSS.new(tree=self.tree)


new = Pyjo_DOM.new
object = Pyjo_DOM  # @ReservedAssignment
