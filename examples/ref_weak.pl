use v5.14;

package C {
use Scalar::Util 'weaken';

    sub new {
        my ($class, $ref) = @_;
        my $self = bless { ref => undef } => $class;
        return $self;
    }

    sub ref {
        my ($self, $ref) = @_;
        $self->{ref} = $ref;
        weaken $self->{ref};
    }

    sub DESTROY {
        warn "DESTROY @_";
    }
}

sub test {
    my $a = C->new;
    my $b = C->new;

    $a->ref($b);
    $b->ref($a);

    warn "$a\->ref = $a->{ref}";
    warn "$b\->ref = $b->{ref}";
}

test();
say "END";
