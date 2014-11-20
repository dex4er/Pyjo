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

my $a = C->new;
my $b = C->new;

$a->ref($b);
$b->ref($a);

warn $a->{ref};
warn $b->{ref};
