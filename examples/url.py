from __future__ import print_function

from Pyjo.URL import *
from Pyjo.Parameters import *

url = Pyjo_URL('https://github.com/dex4er/Pyjo')
print(str(url.set(scheme='ssh+git', userinfo='git', path=str(url.path)+'.git')))

print(Pyjo_URL('http://metacpan.org/search').set(query={'q':'Mojo::URL', 'size':20}).to_string())
