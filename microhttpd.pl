use v5.14;

use Mojo::IOLoop;

my $port = $ARGV[0] || 8080;

my %buffers;

Mojo::IOLoop->server(port => $port, sub {
    my ($loop, $stream, $id) = @_;

    $buffers{$id} = '';

    $stream->on(read => sub {
        my ($stream, $chunk) = @_;

        # Append chunk to buffer
        $buffers{$id} .= $chunk;

        # Check if we got start line and headers (no body support)
        if (index($buffers{$id}, "\x0d\x0a\x0d\x0a") >= 0) {

            my $keepalive = (index($buffers{$id}, "\x0d\x0aConnection: Keep-Alive\x0d\x0a") >= 0);

            # Write a minimal HTTP response
            # (the "Hello World!" message has been optimized away!)
            $stream->write("HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a"
            . ($keepalive ? "Connection: keep-alive\x0d\x0a" : "")
            . "\x0d\x0a");

            if (not $keepalive) {
                $stream->close_gracefully();
            }

            # Clean buffer
            $buffers{$id} = '';
        }
    });
    $stream->on(close => sub {
        delete $buffers{$id};
    });
});

# Start event loop
Mojo::IOLoop->start;

1;
