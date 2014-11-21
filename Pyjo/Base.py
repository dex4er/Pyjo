"""
Pyjo.Base
"""

import importlib


def class_object(_object):
    module_name = _object.__module__
    _object.__name__ = 'object'
    module = importlib.import_module(module_name)
    module.object = _object


@class_object
class _:
    pass
