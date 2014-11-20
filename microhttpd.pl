use Mojo::Base -strict;
use Mojo::IOLoop;

# Minimal ioloop example demonstrating how to cheat at HTTP benchmarks :)
my %buffer;
Mojo::IOLoop->server(
  {port => 8080} => sub {
    my ($loop, $stream, $id) = @_;
    $buffer{$id} = '';
    $stream->on(
      read => sub {
        my ($stream, $chunk) = @_;

        # Append chunk to buffer
        $buffer{$id} .= $chunk;

        # Check if we got start line and headers (no body support)
        if (index($buffer{$id}, "\x0d\x0a\x0d\x0a") >= 0) {

          # Clean buffer
          delete $buffer{$id};

          # Write a minimal HTTP response
          # (the "Hello World!" message has been optimized away!)
          $stream->write("HTTP/1.1 200 OK\x0d\x0aContent-Length: 0\x0d\x0a"
              . "Connection: keep-alive\x0d\x0a\x0d\x0a");
        }
      }
    );
    $stream->on(close => sub { delete $buffer{$id} });
  }
);

# Start event loop
Mojo::IOLoop->start;

1;
