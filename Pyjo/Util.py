"""
Pyjo.Util
"""

from __future__ import print_function

import hashlib
import importlib
import os
import random
import sys
import time


__all__ = ['getenv', 'md5_sum', 'not_implemented', 'lazysingletonmethod',
           'steady_time', 'rand', 'warn']


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


def lazysingletonmethod(method):
    realmethod = method
    while isinstance(realmethod, staticmethod):
        realmethod = realmethod.__func__
    module_name = realmethod.__module__
    method_name = realmethod.__name__
    module = importlib.import_module(module_name)
    def module_method(*args, **kwargs):
        if module.instance is None:
            module_class_name = module.__name__.replace('.', '_')
            module_class = getattr(module, module_class_name)
            module.instance = module_class()
        if isinstance(method, staticmethod):
            module_class_name = module.__name__.replace('.', '_')
            module_class = getattr(module, module_class_name)
            if len(args) > 0 and isinstance(args[0], module_class):
                args = args[1:]
            return realmethod(*args, **kwargs)
        else:
            return method(module.instance, *args, **kwargs)
    setattr(module, method_name, module_method)
    if isinstance(method, staticmethod):
        return staticmethod(module_method)
    return method


def steady_time():
    return time.time()


def rand(value=1):
    return random.random() * value


def warn(*args):
    print(*args, file=sys.stderr)


class Error(Exception):
    pass
