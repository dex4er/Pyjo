use v5.14;

use Mojo::EventEmitter;


package Cat {
    use Mojo::Base 'Mojo::EventEmitter';
    sub poke {
        my ($self, $times) = @_;
        $self->emit(roar => $times);
    }
}


my $tiger = Cat->new();

$tiger->on(roar => sub {
    my ($self, $times) = @_;
    for (1 .. $times) {
        say 'RAWR!';
    }
});

$tiger->poke(2);
$tiger->poke(2);
