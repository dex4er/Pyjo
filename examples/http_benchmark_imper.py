from __future__ import print_function

import sys

import Pyjo.IOLoop
import Pyjo.URL

from Pyjo.Regexp import s
from Pyjo.Util import nonlocals, steady_time


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
url = Pyjo.URL.new(url)

if len(argv) > 1:
    n = int(argv[1])
else:
    n = 1


speeds = []

t0 = steady_time()


print(url)

for i in range(n):

    def on_connect_cb(loop, err, stream):
        on_connect_cb = nonlocals()
        on_connect_cb.size = 0

        def on_read_cb(stream, chunk):
            on_connect_cb.size += len(chunk)
            if verbose:
                print("{0}\r".format(on_connect_cb.size), end='')

        stream.on('read', on_read_cb)

        def on_close_cb(stream):
            t1 = steady_time()
            delta = t1 - t0
            speeds.append(int(on_connect_cb.size * 8 / 1024 / delta / 1000))

            if verbose:
                print(on_connect_cb.size)

        stream.on('close', on_close_cb)

        # Write request
        stream.write("GET {0} HTTP/1.1\x0d\x0aHost: {1}:{2}\x0d\x0a\x0d\x0a".format(url.path, url.host, url.port or 80).encode('ascii'))

    Pyjo.IOLoop.client(address=url.host,
                       port=(url.port or 80),
                       cb=on_connect_cb)


Pyjo.IOLoop.start()


speed = str(sum(speeds))
while True:
    (speed, replaced) = speed == s(r'(?<=\d)(\d{3})(,|$)', r',\1')
    if not replaced:
        break
print('{0} Mb/s'.format(speed))
