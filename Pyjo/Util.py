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


__all__ = ['getenv', 'md5_sum', 'punycode_decode', 'rand', 'steady_time',
           'url_escape', 'url_unescape', 'warn']


def getenv(name, default):
    return os.environ.get(name, default)


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
