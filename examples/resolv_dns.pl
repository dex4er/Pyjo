#!/usr/bin/env perl

use Mojo::IOLoop;
use Net::DNS::Packet;

my $address = $ARGV[0] || 'mojolicio.us';

Mojo::IOLoop->client({address => '8.8.8.8', port => 53, proto => 'udp'} => sub {
    my ($loop, $err, $stream) = @_;
    $stream->on('read' => sub {
      my ($stream, $bytes) = @_;
      my $ans = Net::DNS::Packet->new(\$bytes, 1);
      $stream->close;
    });
    my $packet = Net::DNS::Packet->new($address);
    $stream->write($packet->data);
});

Mojo::IOLoop->start unless Mojo::IOLoop->is_running;
