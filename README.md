[![Build Status](https://travis-ci.org/dex4er/Pyjo.png?branch=master)](https://travis-ci.org/dex4er/Pyjo)

Pyjo
====

A next generation web framework for the Python programming language.

Based on Mojo.


Mojo
====

A next generation web framework for the Perl programming language.

See http://mojolicio.us/


Status
======

Early developement stage. Implemented already:

  * Main event loop which handle IO and timer events
  * Event emitter with subscriptions
  * Synchronizer and sequentializer of multiple events
  * Low level event reactor based on select(2) and poll(2) or libev (pyev)
  * Non-blocking TCP client and server
  * Lazy properties for objects
  * URL parser with container classes for URL, path and querystring
  * Test units with API based on Perl's Test::More and TAP protocol
  * Regexp objects with overloaded operators


Examples
========

URL manipulation
----------------

```python
from __future__ import print_function

import Pyjo.URL
from Pyjo.TextStream import u

url = Pyjo.URL.new(scheme='https', host='github.com', path='/dex4er/Pyjo')
print(url)
# 'https://github.com/dex4er/Pyjo'

print(url.set(scheme='ssh+git', userinfo='git', path=u(url.path) + '.git'))
# 'ssh+git://git@github.com/dex4er/Pyjo.git'
```


Non-blocking TCP client/server
------------------------------

```python
from __future__ import print_function

import Pyjo.IOLoop


# Listen on port 3000
@Pyjo.IOLoop.server(port=3000)
def server(loop, stream, cid):

    @stream.on
    def read(stream, chunk):
        # Process input chunk
        print("Server: {0}".format(chunk.decode('utf-8')))

        # Write response
        stream.write(b"HTTP/1.1 200 OK\x0d\x0a\x0d\x0a")

        # Disconnect client
        stream.close_gracefully()


# Connect to port 3000
@Pyjo.IOLoop.client(port=3000)
def client(loop, err, stream):

    @stream.on
    def read(stream, chunk):
        # Process input
        print("Client: {0}".format(chunk.decode('utf-8')))

    # Write request
    stream.write(b"GET / HTTP/1.1\x0d\x0a\x0d\x0a")


# Add a timer
@Pyjo.IOLoop.timer(3)
def timeouter(loop):
    print("Timeout")
    # Shutdown server
    loop.remove(server)


# Start event loop
Pyjo.IOLoop.start()
```
