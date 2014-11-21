use v5.14;

package C {
    sub new {
        my ($class, $ref) = @_;
        bless { ref => undef } => $class;
    }

    sub ref {
        my ($self, $ref) = @_;
        $self->{ref} = $ref;
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
