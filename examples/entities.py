import Pyjo.UserAgent
from Pyjo.String.Unicode import u

tx = Pyjo.UserAgent.new().get('https://html.spec.whatwg.org')
for n in tx.res.dom('#named-character-references-table tbody > tr').each():
    u(n.at('td > code').text + ' ' + n.children('td')[1].text).trim().say()
