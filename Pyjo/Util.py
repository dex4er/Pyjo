"""
Pyjo.Util
"""

from __future__ import print_function

import hashlib
import os
import random
import sys
import time


__all__ = ['getenv', 'md5_sum', 'not_implemented', 'steady_time', 'rand',
           'warn']


def getenv(name, default):
    return os.environ.get(name, default)


def md5_sum(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def not_implemented(_method):
    def stub(*args, **kwargs):
        raise Error('Method "{0}" not implemented by subclass'.format(_method.__name__))
    return stub


def steady_time():
    return time.time()


def rand(value=1):
    return random.random() * value


def warn(*args):
    print(*args, file=sys.stderr)


class Error(Exception):
    pass
