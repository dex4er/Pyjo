import Pyjo.Server.CGI
from Pyjo.Util import b

cgi = Pyjo.Server.CGI.new()
cgi.unsubscribe('request')


@cgi.on
def request(cgi, tx):
    # Request
    method = tx.req.method
    path = tx.req.url.path

    # Response
    tx.res.code = 200
    tx.res.headers.content_type = 'text/plain'
    tx.res.body = b("{0} request for {1}\n".format(method, path))

    # Resume transaction
    tx.resume()


cgi.run()
