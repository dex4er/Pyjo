use v5.14;

use Mojo::IOLoop;

# Sequentialize multiple events
Mojo::IOLoop->delay->steps(

    # First step (simple timer)
    sub {
        my $delay = shift;
        Mojo::IOLoop->timer(2 => $delay->begin);
        say 'Second step in 2 seconds.';
    },

    # Second step (concurrent timers)
    sub {
        my ($delay, @args) = @_;
        Mojo::IOLoop->timer(1 => $delay->begin);
        Mojo::IOLoop->timer(3 => $delay->begin);
        say 'Third step in 3 seconds.';
    },

    # Third step (the end)
    sub {
        my ($delay, @args) = @_;
        say 'And done after 5 seconds total.';
    }
)->wait;

say "END";
