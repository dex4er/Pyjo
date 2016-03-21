[![Build Status](https://travis-ci.org/dex4er/Pyjoyment.png?branch=master)](https://travis-ci.org/dex4er/Pyjoyment)
[![Documentation Status](https://readthedocs.org/projects/pyjoyment/badge/?version=latest)](http://pyjoyment.readthedocs.org/en/latest/)

Pyjoyment
=========

An asynchronous, event driver web framework for the Python programming language.

Pyjoyment provides own reactor which handles I/O and timer events in its own
main event loop but it supports other loops, ie. EV.

Pyjoyment uses intensively own event emmiter which should be familiar for NodeJS
programmers.

It provides tool set for parsing and creating HTTP messages and HTML documents.
It also supports WSGI interface.

Pyjoyment is compatible with Python 2.7+ and 3.3+. It doesn't require any
external libraries or compilers.

See http://www.pyjoyment.net/

Pyjoyment is based on [Mojolicious](http://mojolicio.us): a next generation
web framework for the Perl programming language.


Status
======

Early developement stage. Implemented already:

  * WSGI adapter
  * HTTP standalone async-io server
  * WebSockets client and server
  * HTTP user agent with TLS/SSL support
  * JSON pointers implementation based on RFC6901
  * Embedded files loader
  * HTML/XML DOM parser with CSS selectors
  * URL parser with container classes for URL, path and querystring
  * Non-blocking TCP client and server
  * Simple logging object
  * Synchronizer and sequentializer of multiple events
  * Main event loop which handle IO and timer events
  * Event emitter with subscriptions
  * Low level event reactor based on select(2) and poll(2)
  * Convenient functions and classed for unicode and byte strings and lists
  * Lazy properties for objects
  * Test units with API based on Perl's Test::More and TAP protocol


Examples
========

Web scraping
------------

```python
import Pyjo.UserAgent
from Pyjo.String.Unicode import u

tx = Pyjo.UserAgent.new().get('https://html.spec.whatwg.org')
for n in tx.res.dom('#named-character-references-table tbody > tr').each():
    u(n.at('td > code').text + ' ' + n.children('td')[1].text).trim().say()
```


URL manipulation
----------------

```python
import Pyjo.URL
from Pyjo.String.Unicode import u

# 'ssh+git://git@github.com/dex4er/Pyjoyment.git'
url = Pyjo.URL.new('https://github.com/dex4er/Pyjoyment')
print(url.set(scheme='ssh+git', userinfo='git', path=u(url.path) + '.git'))

# 'http://metacpan.org/search?q=Mojo::URL&size=20'
print(Pyjo.URL.new('http://metacpan.org/search')
      .set(query={'q': 'Mojo::URL', 'size': 20}))
```


Non-blocking TCP client/server
------------------------------

```python
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
