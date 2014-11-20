from __future__ import print_function

import hashlib
import random
import sys
import time


def md5_sum(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def steady_time():
    return time.time()


def rand(value=1):
    return random.random() * value


def warn(*args):
    print(*args, file=sys.stderr)
