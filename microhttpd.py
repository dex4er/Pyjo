import sys

import Pyjo.IOLoop


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


buffers = {}


def server_cb(loop, stream, cid):
    buffers[cid] = b''

    def on_read_cb(stream, chunk):
        if not cid in buffers:
            buffers[cid] = b''

        # Append chunk to buffer
        buffers[cid] += chunk

        # Check if we got start line and headers (no body support)
        if buffers[cid].find(b"\x0d\x0a\x0d\x0a") >= 0:

            if buffers[cid].find("\x0d\x0aConnection: Keep-Alive\x0d\x0a") >= 0:
                keepalive = True
            else:
                keepalive = False

            # Write a minimal HTTP response
            # (the "Hello World!" message has been optimized away!)
            response = b"HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a"
            if keepalive:
                response += b"Connection: keep-alive\x0d\x0a"
            response += "\x0d\x0a"

            stream.write(response)

            if not keepalive:
                stream.close_gracefully()

            # Clean buffer
            buffers[cid] = b''

    def on_close_cb(stream):
        del buffers[cid]

    stream.on('read', on_read_cb)
    stream.on('close', on_close_cb)

Pyjo.IOLoop.server(port=port, cb=server_cb)

Pyjo.IOLoop.start()
