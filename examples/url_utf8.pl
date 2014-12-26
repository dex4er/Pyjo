use v5.14;
use utf8;

use Mojo::URL;
use Encode;

my $url1 = Mojo::URL->new('http://pl.wikipedia.org')->path('/w/index.php')->query([title=>'Wikipedia:Strona_główna',action=>'history']);
say $url1;

my $url2 = Mojo::URL->new('http://pl.wikipedia.org')->path('/wiki/Wikipedia:Strona_główna');
say $url2;

my $url3 = Mojo::URL->new('http://żółwie.pl');
say $url3;

my $url4 = Mojo::URL->new('http://localhost')->userinfo(encode_utf8('gęślą:jaźń'));
say $url4;
