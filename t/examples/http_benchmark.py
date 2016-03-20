import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # noqa

    import Pyjo.IOLoop
    import Pyjo.URL

    plan(tests=10)

    # Listen on random port
    @Pyjo.IOLoop.server
    def server(loop, stream, cid):

        @stream.on
        def read(stream, chunk):
            # Process input chunk
            is_ok(chunk.decode('utf-8'), "GET / HTTP/1.1\x0d\x0aHost: localhost:{0}\x0d\x0a\x0d\x0a".format(port), "server's input chunk")

            # Write response
            stream.write(b"HTTP/1.1 200 OK\x0d\x0a\x0d\x0a")
            stream.write(b"A" * 1000 * 1000)

            # Disconnect client
            stream.close_gracefully()

    port = Pyjo.IOLoop.acceptor(server).port

    url = Pyjo.URL.new('http://localhost/').set(port=port)
    n = 4

    sizes = []

    pass_ok(url)

    for i in range(n):

        @Pyjo.IOLoop.client(address=url.host, port=(url.port or 80))
        def client(loop, err, stream):
            class context:
                size = 0

            @stream.on
            def read(stream, chunk):
                context.size += len(chunk)

            @stream.on
            def close(stream):
                sizes.append(context.size)

                is_ok(context.size, 19 + 1000 * 1000, 'context.size')

                if len(sizes) == n:
                    Pyjo.IOLoop.remove(server)

            # Write request
            stream.write("GET {0} HTTP/1.1\x0d\x0aHost: {1}:{2}\x0d\x0a\x0d\x0a".format(url.path, url.host, url.port or 80).encode('ascii'))

    Pyjo.IOLoop.start()

    is_ok(sum(sizes), (19 + 1000 * 1000) * 4, 'sum(sizes)')

    done_testing()
