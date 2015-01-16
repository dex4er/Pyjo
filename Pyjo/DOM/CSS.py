# -*- coding: utf-8 -*-

"""
Pyjo.DOM.CSS - CSS selector engine
==================================
::

    import Pyjo.DOM.CSS

    # Select elements from DOM tree
    css = Pyjo.DOM.CSS.new(tree=tree)
    elements = css.select('h1, h2, h3')

:mod:`Pyjo.DOM.CSS` is the CSS selector engine used by :mod:`Pyjo.DOM` and based on
`Selectors Level 3 <http://www.w3.org/TR/css3-selectors/>`_.

Selectors
---------

All CSS selectors that make sense for a standalone parser are supported.

\*
^^

Any element. ::

    all = css.select('*')

E
^

An element of type ``E``. ::

    title = css.select('title')

E[foo]
^^^^^^

An ``E`` element with a ``foo`` attribute. ::

    links = css.select('a[href]')

E[foo="bar"]
^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value is exactly equal to ``bar``. ::

    case_sensitive = css.select('input[type="hidden"]')
    case_sensitive = css.select('input[type=hidden]')

E[foo="bar" i]
^^^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value is exactly equal to any
(ASCII-range) case-permutation of ``bar``. Note that this selector is
EXPERIMENTAL and might change without warning! ::

    case_insensitive = css.select('input[type="hidden" i]')
    case_insensitive = css.select('input[type=hidden i]')
    case_insensitive = css.select('input[class~="foo" i]')

This selector is part of
`Selectors Level 4 <http://dev.w3.org/csswg/selectors-4>`_, which is still a
work in progress.

E[foo~="bar"]
^^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value is a list of
whitespace-separated values, one of which is exactly equal to ``bar``. ::

    foo = css.select('input[class~="foo"]')
    foo = css.select('input[class~=foo]')

E[foo^="bar"]
^^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value begins exactly with the string
``bar``. ::

    begins_with = css.select('input[name^="f"]')
    begins_with = css.select('input[name^=f]')

E[foo$="bar"]
^^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value ends exactly with the string
``bar``. ::

    ends_with = css.select('input[name$="o"]')
    ends_with = css.select('input[name$=o]')

E[foo*="bar"]
^^^^^^^^^^^^^

An ``E`` element whose ``foo`` attribute value contains the substring ``bar``. ::

    contains = css.select('input[name*="fo"]')
    contains = css.select('input[name*=fo]')

E:root
^^^^^^

An ``E`` element, root of the document. ::

    root = css.select(':root')

E:checked
^^^^^^^^^

A user interface element ``E`` which is checked (for instance a radio-button or
checkbox). ::

    input = css.select(':checked')

E:empty
^^^^^^^

An ``E`` element that has no children (including text nodes). ::

    empty = css.select(':empty')

E:nth-child(n)
^^^^^^^^^^^^^^

An ``E`` element, the ``n-th`` child of its parent. ::

    third = css.select('div:nth-child(3)')
    odd   = css.select('div:nth-child(odd)')
    even  = css.select('div:nth-child(even)')
    top3  = css.select('div:nth-child(-n+3)')

E:nth-last-child(n)
^^^^^^^^^^^^^^^^^^^

An ``E`` element, the ``n-th`` child of its parent, counting from the last one. ::

    third    = css.select('div:nth-last-child(3)')
    odd      = css.select('div:nth-last-child(odd)')
    even     = css.select('div:nth-last-child(even)')
    bottom3  = css.select('div:nth-last-child(-n+3)')

E:nth-of-type(n)
^^^^^^^^^^^^^^^^

An ``E`` element, the ``n-th`` sibling of its type. ::

    third = css.select('div:nth-of-type(3)')
    odd   = css.select('div:nth-of-type(odd)')
    even  = css.select('div:nth-of-type(even)')
    top3  = css.select('div:nth-of-type(-n+3)')

E:nth-last-of-type(n)
^^^^^^^^^^^^^^^^^^^^^

An ``E`` element, the ``n-th`` sibling of its type, counting from the last one. ::

    third    = css.select('div:nth-last-of-type(3)')
    odd      = css.select('div:nth-last-of-type(odd)')
    even     = css.select('div:nth-last-of-type(even)')
    bottom3  = css.select('div:nth-last-of-type(-n+3)')

E:first-child
^^^^^^^^^^^^^

An ``E`` element, first child of its parent. ::

    first = css.select('div p:first-child')

E:last-child
^^^^^^^^^^^^

An ``E`` element, last child of its parent. ::

    last = css.select('div p:last-child')

E:first-of-type
^^^^^^^^^^^^^^^

An ``E`` element, first sibling of its type. ::

    first = css.select('div p:first-of-type')

E:last-of-type
^^^^^^^^^^^^^^

An ``E`` element, last sibling of its type. ::

    last = css.select('div p:last-of-type')

E:only-child
^^^^^^^^^^^^

An ``E`` element, only child of its parent. ::

    lonely = css.select('div p:only-child')

E:only-of-type
^^^^^^^^^^^^^^

An ``E`` element, only sibling of its type. ::

    lonely = css.select('div p:only-of-type')

E.warning
^^^^^^^^^

An ``E`` element whose class is "warning". ::

    warning = css.select('div.warning')

E#myid
^^^^^^

An ``E`` element with ``ID`` equal to "myid". ::

    foo = css.select('div#foo')

E:not(s)
^^^^^^^^

An ``E`` element that does not match simple selector ``s``. ::

    others = css.select('div p:not(:first-child)')

E F
^^^

An ``F`` element descendant of an ``E`` element. ::

    headlines = css.select('div h1')

E > F
^^^^^

An ``F`` element child of an ``E`` element. ::

    headlines = css.select('html > body > div > h1')

E + F
^^^^^

An ``F`` element immediately preceded by an ``E`` element. ::

    second = css.select('h1 + h2')

E ~ F
^^^^^

An ``F`` element preceded by an ``E`` element. ::

    second = css.select('h1 ~ h2')

E, F, G
^^^^^^^

Elements of type ``E``, ``F`` and ``G``. ::

    headlines = css.select('h1, h2, h3')

E[foo=bar][bar=baz]
^^^^^^^^^^^^^^^^^^^

An ``E`` element whose attributes match all following attribute selectors. ::

    links = css.select('a[foo^=b][foo$=ar]')
"""


import Pyjo.Base

from Pyjo.Regexp import m, s
from Pyjo.Util import uchr


ESCAPE_RE = r'\\[^0-9a-fA-F]|\\[0-9a-fA-F]{1,6}'
ATTR_RE = r'''
    \[
    ((?:''' + ESCAPE_RE + '''|[\w\-])+)           # Key
    (?:
        (\W)?=                                    # Operator
        (?:"((?:\\"|[^"])*)"|([^\]]+?))           # Value
        (?:\s+(i))?                               # Case-sensitivity
    )?
    \]
'''
PSEUDO_CLASS_RE = r'(?::([\w\-]+)(?:\(((?:\([^)]+\)|[^)])+)\))?)'
TOKEN_RE = r'''
    (\s*,\s*)?                                    # Separator
    ((?:[^[\\:\s,]|''' + ESCAPE_RE + '''\s?)+)?   # Element
    (''' + PSEUDO_CLASS_RE + '''*)?               # Pseudoclass
    ((?:''' + ATTR_RE + ''')*)?                   # Attributes
    (?:\s*([>+~]))?                               # Combinator
'''


class Pyjo_DOM_CSS(Pyjo.Base.object):
    """::

        html = Pyjo.DOM.CSS.new()

    Construct a new :mod:`Pyjo.DOM.CSS` object.
    """

    tree = None
    """::

        tree = html.tree
        html.tree = ['root']

    Document Object Model. Note that this structure should only be used very
    carefully since it is very dynamic.
    """

    def match(self, pattern):
        """::

            bool = css.match('head > title')

        Match CSS selector against first node in :attr:`tree`.
        """
        tree = self.tree
        if tree[0] == 'tag':
            return _match(_compile(pattern), tree, tree)
        else:
            return

    def select(self, pattern):
        """::

            results = css.select('head > title')

        Run CSS selector against :attr:`tree`.
        """
        return _select(False, self.tree, _compile(pattern))

    def select_one(self, pattern):
        """::

            results = css.select_one('head > title')

        Run CSS selector against :attr:`tree` and stop as soon as the first node
        matched.
        """
        return _select(True, self.tree, _compile(pattern))


def _ancestor(selectors, current, tree, pos):
    # TOOD
    return False


def _attr(name_re, value_re, current):
    attrs = current[2]
    for name, value in attrs.items():
        if name == m(name_re):
            if value is not None and value_re is not None:
                if value == m(value_re):
                    return True
            else:
                return True
    return False


def _combinator(selectors, current, tree, pos):
    # Selector
    if len(selectors) > pos:
        c = selectors[pos]
        pos += 1
    else:
        return False

    if isinstance(c, list):
        if not _selector(c, current):
            return False
        if len(selectors) > pos and selectors[pos]:
            c = selectors[pos]
        else:
            return True

    # ">" (parent only)
    if c == '>':
        return _parent(selectors, current, tree, pos)

    # "~" (preceding siblings)
    if c == '~':
        return _sibling(selectors, current, tree, False, pos)

    # "+" (immediately preceding siblings)
    if c == '+':
        return _sibling(selectors, current, tree, True, pos)

    # " " (ancestor)
    return _ancestor(selectors, current, tree, pos)


def _compile(css):
    pattern = [[]]
    for g in m(TOKEN_RE, 'gx').match(css):
        separator, element, pc, attrs, combinator = g[1], g[2], g[3], g[6], g[12]
        if g[2] is None:
            g[2] = ''

        if separator or element or pc or attrs or combinator:
            # New selector
            if separator:
                pattern.append([])
            part = pattern[-1]

            # Empty combinator
            if part and part[-1] and isinstance(part[-1], list):
                part.append(' ')

            # Tag
            selector = []
            part.append(selector)
            element, count, g = element == s('^((?:\\\.|\\\#|[^.#])+)', '')
            if count and g[1] != '*':
                selector.append(['tag', _name(g[1])])

            # Class or ID
            for g in m('(?:([.#])((?:\\[.\#]|[^\#.])+))', 'g').match(element):
                if g[1] == '.':
                    name, op = 'class', '~'
                else:
                    name, op = 'id', ''
                selector.append(['attr', _name(name), _value(op, g[2])])

            # Pseudo classes (":not" contains more selectors)
            for g in m(PSEUDO_CLASS_RE, 'g').match(pc):
                if g[1] == 'not':
                    value = _compile(g[2])
                else:
                    value = _equation(g[2])
                selector.append(['pc', g[1].lower(), value])

            # Attributes
            for g in m(ATTR_RE, 'gx').match(attrs):
                if g[2] is not None:
                    op = g[2]
                else:
                    op = ''
                if g[3] is not None:
                    value = g[3]
                else:
                    value = g[4]
                insensitive = bool(g[5])
                selector.append(['attr', _name(g[1]), _value(op, value, insensitive)])

            # Combinator
            if combinator:
                part.append(combinator)

    return pattern


def _equation(equation):
    if not equation:
        return []

    # "even"
    if equation == m(r'^\s*even\s*$', 'i'):
        return [2, 2]

    # "odd"
    if equation == m(r'^\s*odd\s*$', 'i'):
        return [2, 1]

    # Equation
    num = [1, 1]
    g = equation == m(r'(?:(-?(?:\d+)?)?(n))?\s*\+?\s*(-?\s*\d+)?\s*$', 'i')
    if g:
        if g[1] is not None and len(g[1]):
            num[0] = int(g[1])
        elif g[2]:
            num[0] = 1
        else:
            num[0] = 0
        if num[0] == '-':
            num[0] = -1
        if g[3] is not None:
            num[1] = int(g[3])
        else:
            num[1] = 0

    return num


def _match(pattern, current, tree):
    for p in pattern:
        p.reverse()
        if _combinator(p, current, tree, 0):
            return True
    return False


def _name(value):
    return r'(?:^|:)' + Pyjo.Regexp.re.escape(_unescape(value)) + r'$'


def _parent(selectors, current, tree, pos):
    # TODO
    return False


def _select(one, tree, pattern):
    results = []
    if tree[0] == 'root':
        pos = 1
    else:
        pos = 4
    queue = tree[pos:]
    while queue:
        current = queue.pop(0)
        if current[0] == 'tag':
            queue = current[4:] + queue
            if _match(pattern, current, tree):
                if one:
                    return current
                else:
                    results.append(current)
    if one:
        return
    else:
        return results


def _selector(selector, current):
    for s in selector:
        if s:
            nodetype = s[0]

            # Tag
            if nodetype == 'tag':
                if current[1] != m(s[1]):
                    return False

            # Attribute
            elif nodetype == 'attr':
                if not _attr(s[1], s[2], current):
                    return False

    # TODO
    return True


def _sibling(selectors, current, tree, immediate, pos):
    # TODO
    return False


def _unescape(value):

    # Remove escaped newlines
    value -= s(r'\\n', '', 'g')  # TODO bug in Mojo?

    # Unescape Unicode characters
    value -= s(r'\\([0-9a-fA-F]{1,6})\s?', lambda g: uchr(int(g[1], 16)), 'g')

    # Remove backslash
    value -= s(r'\\', '', 'g')

    return value


def _value(op, value, insensitive=False):
    if value is None:
        return

    value = Pyjo.Regexp.re.escape(_unescape(value))
    if insensitive:
        value = '(?i)' + value

    # "~=" (word)
    if op == '~':
        return r'(?:^|\s+)' + value + '(?:\s+|$)'

    # "*=" (contains)
    if op == '*':
        return value

    # "^=" (begins with)
    if op == '^':
        return r'^' + value

    # "$=" (ends with)
    if op == '$':
        return value + r'$'

    # Everything else
    return r'^' + value + r'$'


new = Pyjo_DOM_CSS.new
object = Pyjo_DOM_CSS  # @ReservedAssignment
