from __future__ import print_function

import Pyjo.IOLoop


# Server
def server_cb(loop, stream, cid):

    def on_read_cb(stream, chunk):
        # Process input chunk
        print("Server: {0}".format(chunk.decode('utf-8')))

        # Write response
        stream.write(b"HTTP/1.1 200 OK\x0d\x0a\x0d\x0a")

        # Disconnect client
        stream.close_gracefully()

    stream.on('read', on_read_cb)

# Listen on port 3000
server = Pyjo.IOLoop.server(port=3000, cb=server_cb)


# Client
def client_cb(loop, err, stream):

    def on_read_cb(stream, chunk):
        # Process input
        print("Client: {0}".format(chunk.decode('utf-8')))

    stream.on('read', on_read_cb)

    # Write request
    stream.write(b"GET / HTTP/1.1\x0d\x0a\x0d\x0a")

# Connect to port 3000
Pyjo.IOLoop.client(port=3000, cb=client_cb)


# Timer
def timer_cb(loop):
    print("Timeout")
    # Shutdown server
    loop.remove(server)

# Add a timer
Pyjo.IOLoop.timer(3, timer_cb)


# Start event loop
Pyjo.IOLoop.start()
