from __future__ import print_function

from Pyjo.URL import *
from Pyjo.Parameters import *

url = Pyjo_URL('https://github.com/dex4er/Pyjo')
print(url.set(scheme='ssh+git', userinfo='git', path=url.path+'.git'))

print(Pyjo_URL('http://metacpan.org/search').set(query={'q':'Mojo::URL', 'size':20}))
