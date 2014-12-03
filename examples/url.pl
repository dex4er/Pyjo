use v5.14;

use Mojo::URL;

my $url = Mojo::URL->new('https://github.com/dex4er/Pyjo');
say $url->scheme('ssh+git')->userinfo('git')->path($url->path.'.git');

say Mojo::URL->new('https://metacpan.org/search')->query(q => 'Mojo::URL', size => 20);
