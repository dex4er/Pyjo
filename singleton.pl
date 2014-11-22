use v5.14;

use Mojo::IOLoop;

say Mojo::IOLoop::singleton;
say Mojo::IOLoop->singleton;
say Mojo::IOLoop->new->singleton;
