import Pyjo.UserAgent

import sys

try:
    url = sys.argv[1]
except IndexError:
    raise Exception('get.py url opts')

opts = dict(map(lambda a: a.split('='), sys.argv[2:]))

tx = Pyjo.UserAgent.new(**opts).get(url)
print(tx.res.text)
