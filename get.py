import Pyjo.IOLoop


def client_cb(loop, err, stream):
    def read_cb(stream, chunk):
        print(chunk.decode('utf-8'))
        stream.close()
    stream.on('read', read_cb)
    stream.write(b"GET / HTTP/1.0\x0d\x0a\x0d\x0a")

Pyjo.IOLoop.client(address='127.0.0.1', port=80, cb=client_cb)

Pyjo.IOLoop.start()
