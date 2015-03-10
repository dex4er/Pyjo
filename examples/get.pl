use v5.14;

use Mojo::UserAgent;

my $url = shift @ARGV or die 'get.pl url opts';
my %opts = map { split /=/, $_, 2 } @ARGV;

my $tx = Mojo::UserAgent->new(%opts)->get($url);
say $tx->res->text;
