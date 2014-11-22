"""
Pyjo.Base
"""

import importlib


def modulemethod(_method):
    module_name = _method.__module__
    method_name = _method.__name__
    module = importlib.import_module(module_name)
    def module_method(*args, **kwargs):
        if module.instance is None:
            module.instance = module.object()
        return getattr(module.instance, method_name)(*args, **kwargs)
    setattr(module, method_name, module_method)
    return _method


def moduleobject(_object):
    _object.__name__ = 'object'
    module_name = _object.__module__
    module = importlib.import_module(module_name)
    module.object = _object
    return module.object


@moduleobject
class Pyjo_Base:
    pass
