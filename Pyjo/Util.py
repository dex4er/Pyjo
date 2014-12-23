"""
Pyjo.Util
"""

from __future__ import print_function

import hashlib
import os
import random
import sys
import time

from Pyjo.Regexp import s


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


def getenv(name, default):
    return os.environ.get(name, default)


def has(attrs, default=None, *args):
    return lambda cls: cls.attr(attrs, default)


class lazy(object):
    def __init__(self, default=None, name=None):
        self.default = default
        self.name = name

    def __get__(self, obj, objtype):
        print('get', self, obj, objtype)
        if obj is None:
            return self
        if callable(self.default):
            default = self.default(obj if obj is not None else objtype)
        else:
            default = self.default
        if self.name is None:
            return default
        setattr(obj, self.name, default)
        return getattr(obj, self.name)


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
    return bytes(string, 'ascii').decode('punycode')


def punycode_encode(string):
    return string.encode('punycode').decode('ascii')


def rand(value=1):
    return random.random() * value


def steady_time():
    return time.time()


def url_escape(string, pattern=None):
    if pattern is not None:
        pattern = '([{0}])'.format(pattern)
    else:
        pattern = '([^A-Za-z0-9\-._~])'

    return string == s(pattern, lambda m: '%' + format(ord(m[1]), 'X'), 'gr')


def url_unescape(string):
    return string == s('%([0-9a-fA-F]{2})', lambda m: chr(int(m[1], 16)), 'gr')


def warn(*args):
    print(*args, file=sys.stderr)
