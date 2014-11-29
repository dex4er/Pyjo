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


__all__ = ['getenv', 'md5_sum', 'not_implemented', 'steady_time', 'rand',
           'url_escape', 'warn']


def getenv(name, default):
    return os.environ.get(name, default)


def md5_sum(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def steady_time():
    return time.time()


def rand(value=1):
    return random.random() * value


re_url_escape_pattern = re.compile(r'([^A-Za-z0-9\-._~])')


def url_escape(string, pattern=None):
    if pattern is not None:
        r = re.compile(r'([' + pattern + '])')
    else:
        r = re_url_escape_pattern

    return r.sub(lambda m: '%' + format(ord(m.group(1)), 'X'), string)


def warn(*args):
    print(*args, file=sys.stderr)
