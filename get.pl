use Mojo::IOLoop;

Mojo::IOLoop->client(
  {address, '127.0.0.1', port => 80} => sub {
    my ($loop, $err, $stream) = @_;
    $stream->on(
      read => sub {
        my ($stream, $chunk) = @_;
        print $chunk;
        $stream->close();
      }
    );
    $stream->write("GET / HTTP/1.0\x0d\x0a\x0d\x0a");
  }
);

Mojo::IOLoop->start;
