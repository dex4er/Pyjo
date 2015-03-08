import Pyjo.UserAgent

import sys

tx = Pyjo.UserAgent.new().get(sys.argv[1])
print(tx.res.text)
