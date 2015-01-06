"""
Pyjo.Util
"""

from __future__ import print_function

import hashlib
import os
import random
import sys
import time

from Pyjo.ByteStream import b
from Pyjo.Regexp import s
from Pyjo.TextStream import u


class Error(Exception):
    pass


def decorator(func):
    def wrap(*args):
        if not callable(args[0]):
            def wrap2(func2):
                return func(func2, *args)
            return wrap2
        return func(*args)
    return wrap


def decoratormethod(func):
    def wrap(self, *args):
        if not callable(args[0]):
            def wrap2(func2):
                return func(self, func2, *args)
            return wrap2
        return func(self, *args)
    return wrap


def dictget(d, *k):
    return [d[i] for i in k]


def getenv(name, default):
    return os.environ.get(name, default)


def isbytes(obj):
    return isinstance(obj, bytes) and not isinstance(obj, str)


def isiterable(obj):
    return hasattr(obj, '__iter__')


def isstr(obj):
    return isinstance(obj, str)


def isiterable_not_str(obj):
    return not isstr(obj) and isiterable(obj)


def md5_sum(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


class nonlocals(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def not_implemented(method):
    def stub(*args, **kwargs):
        raise Error('Method "{0}" not implemented by subclass'.format(method.__name__))
    return stub


def punycode_decode(string):
    return b(string, 'iso-8859-1').decode('punycode')


def punycode_encode(string):
    return u(string).encode('punycode')


def rand(value=1):
    return random.random() * value


def steady_time():
    return time.time()


def url_escape(string, pattern=None):
    if pattern is not None:
        if isinstance(pattern, bytes):
            pattern = b'([' + b(pattern, 'iso-8859-1') + b'])'
        else:
            pattern = '([{0}])'.format(pattern)
    else:
        pattern = '([^A-Za-z0-9\-._~])'

    if isinstance(string, bytes):
        pattern = b(pattern, 'iso-8859-1')
        replacement = lambda m: b('%' + format(ord(m[1]), 'X'), 'iso-8859-1')
    else:
        replacement = lambda m: '%' + format(ord(m[1]), 'X')

    return b(string == s(pattern, replacement, 'gr'), 'iso-8859-1').decode('iso-8859-1')


def url_unescape(string):
    return b(string) == s(br'%([0-9a-fA-F]{2})', lambda m: b(chr(int(m[1], 16)), 'iso-8859-1'), 'gr')


def warn(*args):
    print(*args, file=sys.stderr)
