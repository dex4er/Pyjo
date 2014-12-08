from __future__ import print_function

import re
import sys

import Pyjo.IOLoop
import Pyjo.URL

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

    @Pyjo.IOLoop.client(address=url.host, port=(url.port or 80))
    def client(loop, err, stream):
        client = nonlocals()
        client.size = 0

        @stream.on
        def read(stream, chunk):
            client.size += len(chunk)
            if verbose:
                print("{0}\r".format(client.size), end='')

        @stream.on
        def close(stream):
            t1 = steady_time()
            delta = t1 - t0
            speeds.append(int(client.size * 8 / 1024 / delta / 1000))

            if verbose:
                print(client.size)

        # Write request
        stream.write("GET {0} HTTP/1.1\x0d\x0aHost: {1}:{2}\x0d\x0a\x0d\x0a".format(url.path, url.host, url.port or 80).encode('ascii'))


Pyjo.IOLoop.start()


speed = str(sum(speeds))
while True:
    (speed, replaced) = re.subn(r'(?<=\d)(\d{3})(,|$)', r',\1', speed)
    if not replaced:
        break
print('{0} Mb/s'.format(speed))
