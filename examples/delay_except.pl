use v5.14;

use Mojo::IOLoop;

# Handle exceptions in all steps
Mojo::IOLoop::Delay->new->steps(
    sub {
        my $delay = shift;
        die 'Intentional error';
    },
    sub {
        my ($delay, @args) = @_;
        say 'Never actually reached.';
    }
)->catch(sub {
    my ($delay, $err) = @_;
    say "Something went wrong: $err";
})->wait;
