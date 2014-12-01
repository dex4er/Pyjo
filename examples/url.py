from __future__ import print_function

from Pyjo.URL import *

url = Pyjo_URL('https://github.com/dex4er/Pyjo')
print(str(url.set(scheme='ssh+git', userinfo='git', path=str(url.path)+'.git')))
