import sys

import Pyjo.IOLoop


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


@Pyjo.IOLoop.server(address='0.0.0.0', port=port)
def server(loop, stream, cid):

    @stream.on
    def read(stream, chunk):
        # Check if we got start line and headers (no body support)
        if chunk.find(b"\x0d\x0a\x0d\x0a") >= 0:

            if chunk.find(b"\x0d\x0aConnection: Keep-Alive\x0d\x0a") >= 0:
                keepalive = True
            else:
                keepalive = False

            # Write a minimal HTTP response
            # (the "Hello World!" message has been optimized away!)
            response = b"HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a"
            if keepalive:
                response += b"Connection: keep-alive\x0d\x0a"
            response += b"\x0d\x0a"

            stream.write(response)

            if not keepalive:
                stream.close_gracefully()


Pyjo.IOLoop.start()
