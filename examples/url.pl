use v5.14;

use Mojo::URL;

my $url = Mojo::URL->new('https://github.com/dex4er/Pyjo');
say $url->scheme('ssh+git')->userinfo('git')->path($url->path.'.git');
