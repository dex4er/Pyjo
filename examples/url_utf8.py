# -*- coding: utf-8 -*-

from __future__ import print_function

import Pyjo.URL

url1 = Pyjo.URL.new('http://pl.wikipedia.org').set(path='/w/index.php', query=[('title', u'Wikipedia:Strona_główna'), ('action', 'history')])
print(url1)

url2 = Pyjo.URL.new('http://pl.wikipedia.org').set(path=u'/wiki/Wikipedia:Strona_główna')
print(url2)

url3 = Pyjo.URL.new(u'http://żółwie.pl')
print(url3)

url4 = Pyjo.URL.new(u'http://localhost').set(userinfo=u'gęślą:jaźń')
print(url4)
