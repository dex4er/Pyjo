"""
Pyjo.Util
"""

from __future__ import print_function

import hashlib
import os
import random
import re
import sys
import time


__all__ = ['getenv', 'has', 'lazy', 'md5_sum', 'punycode_decode', 'rand',
           'steady_time', 'url_escape', 'url_unescape', 'warn']

def has(attrs, default=None, *args):
    return lambda cls: cls.attr(attrs, default)


def getenv(name, default):
    return os.environ.get(name, default)


class lazy(object):
    def __init__(self, default=None, name=None):
        self.default = default
        self.name = name

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        if callable(self.default):
            default = self.default()
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


def punycode_decode(string):
    return bytes(string, 'ascii').decode('punycode')


def punycode_encode(string):
    return string.encode('punycode').decode('ascii')


def steady_time():
    return time.time()


def rand(value=1):
    return random.random() * value


re_url_escape_pattern = re.compile(r'([^A-Za-z0-9\-._~])')
re_url_unescape_pattern = re.compile(r'%([0-9a-fA-F]{2})')

def url_escape(string, pattern=None):
    if pattern is not None:
        r = re.compile(r'([' + pattern + '])')
    else:
        r = re_url_escape_pattern

    return r.sub(lambda m: '%' + format(ord(m.group(1)), 'X'), string)


def url_unescape(string):
    return re_url_unescape_pattern.sub(lambda m: chr(int(m.group(1), 16)), string)


def warn(*args):
    print(*args, file=sys.stderr)
