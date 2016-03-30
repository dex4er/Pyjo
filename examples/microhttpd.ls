#!/usr/bin/env lsc

global import require 'prelude-ls'

require! {
  'net'
}

opts = pairs-to-obj map (split '='), concat [['address=127.0.0.1', 'port=8080'], process.argv.slice(2)]

server = net.createServer (socket) ->
  socket.on 'data', (chunk) ->
    # Check if we got start line and headers (no body support)
    if chunk.indexOf("\x0d\x0a\x0d\x0a") >= 0
      keepalive = chunk.indexOf("\x0d\x0aConnection: Keep-Alive\x0d\x0a") >= 0

      # Write a minimal HTTP response
      # (the "Hello World!" message has been optimized away!)
      socket.write "HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a" +
        (if keepalive then "Connection: keep-alive\x0d\x0a" else "") +
        "\x0d\x0a"

      if not keepalive
        socket.destroy()

server.listen(opts.port, opts.address)
