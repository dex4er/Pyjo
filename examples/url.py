from __future__ import print_function

import Pyjo.URL
from Pyjo.Util import text

url = Pyjo.URL.new('https://github.com/dex4er/Pyjo')
print(url.set(scheme='ssh+git', userinfo='git', path=text(url.path) + '.git'))

print(Pyjo.URL.new('http://metacpan.org/search')
      .set(query={'q': 'Mojo::URL', 'size': 20}))
