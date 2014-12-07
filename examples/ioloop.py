from __future__ import print_function

import Pyjo.IOLoop


# Listen on port 3000
@Pyjo.IOLoop.register('server')
@Pyjo.IOLoop.server(port=3000)
def server_cb(loop, stream, cid):

    @Pyjo.IOLoop.on(stream, 'read')
    def on_read_cb(stream, chunk):
        # Process input chunk
        print("Server: {0}".format(chunk.decode('utf-8')))

        # Write response
        stream.write(b"HTTP/1.1 200 OK\x0d\x0a\x0d\x0a")

        # Disconnect client
        stream.close_gracefully()


# Connect to port 3000
@Pyjo.IOLoop.client(port=3000)
def client_cb(loop, err, stream):

    @Pyjo.IOLoop.on(stream, 'read')
    def on_read_cb(stream, chunk):
        # Process input
        print("Client: {0}".format(chunk.decode('utf-8')))

    # Write request
    stream.write(b"GET / HTTP/1.1\x0d\x0a\x0d\x0a")


# Add a timer
@Pyjo.IOLoop.timer(3)
def timer_cb(loop):
    print("Timeout")
    # Shutdown server
    loop.remove('server')


# Start event loop
Pyjo.IOLoop.start()
