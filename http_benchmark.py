from __future__ import print_function

import re
import sys

import Pyjo.IOLoop

from Pyjo.URL import *

from Pyjo.Util import steady_time

argv = sys.argv[1:]

if len(argv) > 0 and (argv[0] == '-v' or argv[0] == '--verbose'):
    argv.pop(0)
    verbose = True
else:
    verbose = False

if len(argv) > 0:
    url = argv[0]
else:
    url = 'http://localhost/bigfile.bin'
url = Pyjo_URL(url)

if len(argv) > 1:
    n = int(argv[1])
else:
    n = 1


speeds = [0 for i in range(n)]
sizes = [0 for i in range(n)]

t0 = steady_time()

def client_cb(loop, err, stream):

    def on_read_cb(stream, chunk):
        sizes[i] += len(chunk)
        if verbose:
            print("{0}\r".format(sizes[i]), end='')

    stream.on('read', on_read_cb)

    def on_close_cb(stream):
        t1 = steady_time()
        delta = t1 - t0
        speeds.append(int(sizes[i] * 8 / 1024 / delta / 1000))

        if verbose:
            print(sizes[i])

        speed = str(sum(speeds))
        while True:
            (speed, replaced) = re.subn(r'(?<=\d)(\d{3})(,|$)', r',\1', speed)
            if not replaced:
                break
        print('{0} Mb/s'.format(speed))

    stream.on('close', on_close_cb)

    # Write request
    stream.write("GET {0} HTTP/1.1\x0d\x0aHost: {1}:{2}\x0d\x0a\x0d\x0a".format(url.path, url.host, url.port or 80).encode('ascii'))


for i in range(n):
    Pyjo.IOLoop.client(address=url.host, port=(url.port or 80), cb=client_cb)

while not Pyjo.IOLoop.is_running():
    Pyjo.IOLoop.start()
