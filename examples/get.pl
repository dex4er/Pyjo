use v5.14;

use Mojo::UserAgent;

my $tx = Mojo::UserAgent->new->get($ARGV[0]);
say $tx->res->text;
