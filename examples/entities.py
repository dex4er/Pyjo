import Pyjo.UserAgent
from Pyjo.String.Unicode import u

tx = Pyjo.UserAgent.new().get('https://html.spec.whatwg.org')
for n in tx.res.dom('#named-character-references-table tbody > tr').each():
    name = u(n.at('td > code').text).trim()
    char = ''
    for c in u(n.children('td')[1].text).trim().split(' '):
        c = int(c.replace('U+', ''), 16)
        if c < 0x80:
            c = '"\\x{0:02x}"'.format(c)
        elif c < 0x100:
            c = 'u"\\x{0:02x}"'.format(c)
        elif c < 0x10000:
            c = 'u"\\u{0:04x}"'.format(c)
        else:
            c = 'u"\\U{0:08x}"'.format(c)
        char += c
    u('    "{0}": {1},'.format(name, char)).say()
