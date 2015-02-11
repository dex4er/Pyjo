import socket
import ssl
import pprint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s)
#                           ca_certs="server.crt",
#                           cert_reqs=ssl.CERT_REQUIRED,
#                           ciphers="ALL:aNULL:eNULL",)
#)

ssl_sock.connect(('localhost', 443))

print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())

# Set a simple HTTP request -- use httplib in actual code.
ssl_sock.write("""GET / HTTP/1.0\r
Host: www.debian.org\n\n""")

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
data = ssl_sock.read()

print(data)

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()
