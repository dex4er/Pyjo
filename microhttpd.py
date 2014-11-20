import sys

import Pyjo.IOLoop


def server(loop, stream, tid):
    print(loop, stream, tid)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

Pyjo.IOLoop.server(port=port, cb=server)
Pyjo.IOLoop.start()
