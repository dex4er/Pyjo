use v5.14;

use AE;
use AnyEvent::Socket;
use AnyEvent::Handle;

my %opts = (address => '0.0.0.0', port => 8080, map { split /=/, $_, 2 } @ARGV);

my %connections;

tcp_server $opts{address}, $opts{port}, sub {
    my ($fh) = @_;
    my $handle = AnyEvent::Handle->new(
        fh => $fh,
        poll => 'r',
    );
    $handle->on_read(sub {
        my $chunk = $handle->rbuf;

        # Check if we got start line and headers (no body support)
        if (index($chunk, "\x0d\x0a\x0d\x0a") >= 0) {

            my $keepalive = (index($chunk, "\x0d\x0aConnection: Keep-Alive\x0d\x0a") >= 0);

            # Write a minimal HTTP response
            # (the "Hello World!" message has been optimized away!)
            $handle->push_write("HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a"
            . ($keepalive ? "Connection: keep-alive\x0d\x0a" : "")
            . "\x0d\x0a");

            if (not $keepalive) {
                delete $connections{$handle};
                $handle->destroy();
            }
        }
    });
    $handle->on_eof(sub {
        undef $handle;
    });
    $handle->on_error(sub {
        undef $handle;
    });
};

# Start event loop
AE::cv->recv;
