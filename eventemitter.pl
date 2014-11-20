use v5.14;

use Mojo::EventEmitter;


package Cat {
    use Mojo::Base 'Mojo::EventEmitter';
    sub poke {
        my ($self) = @_;
        $self->emit(roar => 3);
    }
}


my $tiger = Cat->new();

$tiger->on(roar => sub {
    my ($name, $times) = @_;
    for (1 .. $times) {
        say 'RAWR!';
    }
});

$tiger->poke();
