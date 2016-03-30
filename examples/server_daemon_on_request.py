import Pyjo.Server.Daemon
from Pyjo.Util import b

with Pyjo.Server.Daemon.new(listen=['http://*:3000']) as daemon:
    daemon.unsubscribe('request')

    @daemon.on
    def request(daemon, tx):
        # Request
        method = tx.req.method
        path = tx.req.url.path

        # Response
        tx.res.code = 200
        tx.res.headers.content_type = 'text/plain'
        tx.res.body = b("{0} request for {1}\n".format(method, path))

        # Resume transaction
        tx.resume()

    daemon.run()
