use v5.14;
use lib '/home/dexter/perl5/lib/perl5';

use Mojo::IOLoop;

Mojo::IOLoop->recurring(0, sub {
    say "A";
});

Mojo::IOLoop->timer(1, sub {
    my ($loop) = @_;
    say "OOPS!";
    $loop->reactor->emit(error => 'BOOM!');
    #$loop->stop();
});

Mojo::IOLoop->start();
