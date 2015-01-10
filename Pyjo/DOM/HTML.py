# -*- coding: utf-8 -*-

"""
Pyjo.DOM.HTML - HTML/XML engine
===============================
::

    import Pyjo.DOM.HTML

    html = Pyjo.DOM.HTML.new()
    html.parse('<div><p id="a">Test</p><p id="b">123</p></div>')
    tree = html.tree
"""


import Pyjo.Base
import Pyjo.TextStream

from Pyjo.Base import lazy
from Pyjo.Regexp import m
from Pyjo.Util import html_unescape, xml_escape


ATTR_RE = r'''
  ([^<>=\s\/]+|\/)   # Key
  (?:
    \s*=\s*
    (?:
      "([^"]*?)"     # Quotation marks
    |
      '([^']*?)'     # Apostrophes
    |
      ([^>\s]*)      # Unquoted
    )
  )?
  \s*
'''

TOKEN_RE = r'''
  ([^<]+)?                                            # Text
  (?:
    <(?:
      !(?:
        DOCTYPE(
        \s+\w+                                        # Doctype
        (?:(?:\s+\w+)?(?:\s+(?:"[^"]*"|'[^']*'))+)?   # External ID
        (?:\s+\[.+?\])?                               # Int Subset
        \s*)
      |
        --(.*?)--\s*                                  # Comment
      |
        \[CDATA\[(.*?)\]\]                            # CDATA
      )
    |
      \?(.*?)\?                                       # Processing Instruction
    |
      \s*([^<>\s]+\s*(?:(?:''' + ATTR_RE + '''){0,32766})*+)     # Tag
    )>
  |
    (<)                                               # Runaway "<"
  )??
'''

# HTML elements that only contain raw text
RAW = {'script', 'style'}

# HTML elements that only contain raw text and entities
RCDATA = {'title', 'textarea'}

# HTML elements with optional end tags
END = {'body': 'head', 'optgroup': 'optgroup', 'option': 'option'}

# HTML elements that break paragraphs
for _ in ('address', 'article', 'aside', 'blockquote', 'dir', 'div', 'dl',
          'fieldset', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
          'header', 'hr', 'main', 'menu', 'nav', 'ol', 'p', 'pre', 'section',
          'table', 'ul'):
    END[_] = 'p'

# HTML table elements with optional end tags
TABLE = {'colgroup', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'}

# HTML elements with optional end tags and scoping rules
CLOSE = {'li': ({'li'}, {'ul', 'ol'}),
         'tr': ({'tr'}, {'table'}),
         'colgroup': [TABLE],
         'tbody': [TABLE],
         'tfoot': [TABLE],
         'thead': [TABLE],
         'dd': ({'dd', 'dt'}, {'dl'}),
         'dt': ({'dd', 'dt'}, {'dl'}),
         'rp': ({'rp', 'rt'}, {'ruby'}),
         'rt': ({'rp', 'rt'}, {'ruby'}),
         'td': ({'th', 'td'}, {'table'}),
         'th': ({'th', 'td'}, {'table'}),
         }

# HTML elements without end tags
EMPTY = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
         'keygen', 'link', 'menuitem', 'meta' 'param', 'source', 'track',
         'wbr'}

# HTML elements categorized as phrasing content (and obsolete inline elements)
PHRASING = {'a', 'abbr', 'area', 'audio', 'b', 'bdi', 'bdo', 'br', 'button',
            'canvas', 'cite', 'code', 'data', 'datalist', 'del', 'dfn', 'em',
            'embed', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'keygen',
            'label', 'link', 'map', 'mark', 'math', 'meta', 'meter',
            'noscript', 'object', 'output', 'picture', 'progress', 'q',
            'ruby', 's', 'samp', 'script', 'select', 'small', 'span',
            'strong', 'sub', 'sup', 'svg', 'template', 'textarea', 'time',
            'u', 'var', 'video', 'wbr'}

OBSOLETE = {'acronym', 'applet', 'basefont', 'big', 'font', 'strike', 'tt'}
PHRASING = OBSOLETE | PHRASING

# HTML elements that don't get their self-closing flag acknowledged
BLOCK = {'a', 'address', 'applet', 'article', 'aside', 'b', 'big',
         'blockquote', 'body', 'button', 'caption', 'center', 'code', 'col',
         'colgroup', 'dd', 'details', 'dialog', 'dir', 'div', 'dl', 'dt',
         'em', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form',
         'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header',
         'hgroup', 'html', 'i', 'iframe', 'li', 'listing', 'main', 'marquee',
         'menu', 'nav', 'nobr', 'noembed', 'noframes', 'noscript', 'object',
         'ol', 'optgroup', 'option', 'p', 'plaintext', 'pre', 'rp', 'rt',
         's', 'script', 'section', 'select', 'small', 'strike', 'strong',
         'style', 'summary', 'table', 'tbody', 'td', 'template', 'textarea',
         'tfoot', 'th', 'thead', 'title', 'tr', 'tt', 'u', 'ul', 'xmp'}


class Pyjo_DOM_HTML(Pyjo.Base.object):
    """::

        html = Pyjo.DOM.HTML.new()

    Construct a new :mod:`Pyjo.DOM.HTML` object.
    """

    tree = lazy(lambda self: ['root'])
    """::

        tree = html.tree
        html.tree = ['root']

    Document Object Model. Note that this structure should only be used very
    carefully since it is very dynamic.
    """

    xml = None
    """::

        bool = html.xml
        html.xml = bool

    Disable HTML semantics in parser and activate case sensitivity, defaults to
    auto detection based on processing instructions.
    """

    def parse(self, html):
        """::

            html = html.parse(u'<foo bar="baz">I ♥ Mojolicious!</foo>')

        Parse HTML/XML fragment.
        """
        xml = self.xml
        tree = ['root']
        current = tree
        text = None

        pos = 0
        while True:
            prevpos = pos
            matchiter = html[pos:] == m('^' + TOKEN_RE, 'cgisx')
            if not matchiter:
                break
            for g in matchiter:
                text, doctype, comment, cdata, pi, tag, runaway = g[1], g[2], g[3], g[4], g[5], g[6], g[11]

                pos += g['end']

                # Text (and runaway "<")
                if runaway is not None and text is not None:
                    text += '<'

                if text is not None:
                    node = _node(current, 'text', html_unescape(text))
                    if node:
                        current = node

                # Tag
                if tag is not None:

                    # End
                    g = tag == m(r'^\/\s*(\S+)')
                    if g:
                        current = _end(g[1] if xml else g[1].lower(), xml, current)

                    # Start
                    else:
                        g = tag == m(r'^([^\s/]+)([\s\S]*)')
                        if g:
                            start, attr = g[1], g[2]
                            if not xml:
                                start = start.lower()

                            attrs = {}
                            closing = False

                            # Attributes
                            for g in m(ATTR_RE, 'gx').match(attr):
                                key = g[1]
                                if g[2] is not None:
                                    value = g[2]
                                elif g[2] is not None:
                                    value = g[3]
                                else:
                                    value = g[4]

                                # Empty tag
                                if key == '/':
                                    closing = True
                                    continue

                                if value is not None:
                                    attrs[key] = html_unescape(value)
                                else:
                                    attrs[key] = value

                            # "image" is an alias for "img"
                            if not xml and start == 'image':
                                start = 'img'

                            current = _start(start, attrs, xml, current)

                            # Element without end tag (self-closing)
                            if not xml and start in EMPTY or (xml or start not in BLOCK) and closing:
                                current = _end(start, xml, current)

                            # Raw text elements
                            if xml or start not in RAW and start not in RCDATA:
                                continue
                            g = html[pos:] == m(r'^(.*?)<\s*/\s*' + start + '\s*>', 'is')
                            if not g:
                                continue
                            pos += g['end']
                            node = _node(current, 'raw', html_unescape(g[1]) if start in RCDATA else g[1])
                            if node:
                                current = node
                            current = _end(start, 0, current)

                # DOCTYPE
                elif doctype is not None:
                    node = _node(current, 'doctype', doctype)
                    if node:
                        current = node

                # Comment
                elif comment is not None:
                    node = _node(current, 'comment', comment)
                    if node:
                        current = node

                # CDATA
                elif cdata is not None:
                    node = _node(current, 'cdata', cdata)
                    if node:
                        current = node

                # Processing instruction (try to detect XML)
                elif pi is not None:
                    if self.xml is None and pi == m('xml', 'i'):
                        xml = True
                        self.xml = xml
                    node = _node(current, 'pi', pi)
                    if node:
                        current = node

            if pos == prevpos:
                break

        self.tree = tree
        return self

    def render(self):
        """::

            string = html.render()

        Render DOM to HTML/XML. Returns :mod:`Pyjo.TextStream` object.
        """
        return Pyjo.TextStream.new(_render(self.tree, self.xml))


def _end(end, xml, current):

    # Search stack for start tag
    nextnode = current
    while True:
        # Ignore useless end tag
        if nextnode[0] == 'root':
            return

        # Right tag
        if nextnode[1] == end:
            return nextnode[3]

        # Phrasing content can only cross phrasing content
        if not xml and end in PHRASING and nextnode[1] not in PHRASING:
            return

        nextnode = nextnode[3]
        if nextnode is None:
            break


def _node(current, nodetype, content):
    new = [nodetype, content, current]  # TODO weakref new[2]
    current.append(new)
    return current


def _render(tree, xml):
    nodetype = tree[0]

    # Text (escaped)
    if nodetype == 'text':
        return xml_escape(tree[1])

    # Raw text
    if nodetype == 'raw':
        return tree[1]

    # DOCTYPE
    if nodetype == 'doctype':
        return '<!DOCTYPE' + tree[1] + '>'

    # Comment
    if nodetype == 'comment':
        return '<!--' + tree[1] + '-->'

    # CDATA
    if nodetype == 'cdata':
        return '<![CDATA[' + tree[1] + ']]>'

    # Processing instruction
    if nodetype == 'pi':
        return '<?' + tree[1] + '?>'

    # Start tag
    result = ''
    if nodetype == 'tag':
        # Open tag
        tag = tree[1]
        result += '<' + tag

        # Attributes
        attrs = []

        for key in sorted(tree[2].keys()):
            # No value
            if key not in tree[2] or not tree[2][key]:
                attrs.append(key)
            else:
                value = tree[2][key]
                attrs.append(key + '="' + xml_escape(value) + '"')

        if attrs:
            result += ' ' + ' '.join(attrs)

        # Element without end tag
        if len(tree) <= 4:
            if xml:
                return result + ' />'
            elif tag in EMPTY:
                return result + '>'
            else:
                return result + '></' + tag + '>'

        # Close tag
        result += '>'

    # Render whole tree
    if nodetype == 'root':
        start = 1
    else:
        start = 4
    for t in tree[start:]:
        result += _render(t, xml)

    # End tag
    if nodetype == 'tag':
        result += '</' + tree[1] + '>'

    return result


def _start(start, attrs, xml, current):
    # Autoclose optional HTML elements
    if not xml and current[0] != 'root':
        if start in END:
            node = _end(END[start], 0, current)
            if node:
                current = node
        elif start in CLOSE:
            allowed, scope = CLOSE[start]

            # Close allowed parent elements in scope
            parent = current
            while parent[0] != 'root' and not scope[parent[1]]:
                if allowed[parent[1]]:
                    node = _end(parent[1], 0, current)
                    if node:
                        current = node
                    parent = parent[3]

    # New tag
    new = ['tag', start, attrs, current]
    current.append(new)
    return new


new = Pyjo_DOM_HTML.new
object = Pyjo_DOM_HTML  # @ReservedAssignment
