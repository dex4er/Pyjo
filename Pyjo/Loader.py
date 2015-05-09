# -*- coding: utf-8 -*-

"""
Pyjo.Loader - Loader
====================
::

    from Pyjo.Loader import module_data, find_modules, load_module

    # Find modules in a namespace
    for module in find_modules('Some.Namespace'):

        # Load them safely
        try:
            load_class(module)
        except ImportError as e:
            print('Loading "{0}" failed: {1}'.format(module, e))

        # And extract files from the DATA section
        print(data_section(module, 'some_file.txt'))

:mod:`Pyjo.Loader` is a module loader and plugin framework. Aside from finding
modules and loading classes, it allows multiple files to be stored in the
``DATA`` variable of a module, which can then be accessed individually. ::

    # Some/Namespace/Module.py

    DATA = r'''

    @@ test.txt
    This is the first file.

    @@ test2.html (base64)
    VGhpcyBpcyB0aGUgc2Vjb25kIGZpbGUu

    @@ test
    This is the
    third file.
    '''

Each file has a header starting with ``@@``, followed by the file name and
optional instructions for decoding its content. Currently only the Base64
encoding is supported, which can be quite convenient for the storage of binary
data.

Functions
---------
"""

import importlib

from Pyjo.Regexp import r
from Pyjo.Util import b64_decode


BIN = {}
CACHE = {}


re_files = r(r'^@@\s*(.+?)\s*\r?\n', 'm')
re_base64 = r(r'\s*\(\s*base64\s*\)$')


def embedded_file(modname, filename=None):
    """::

        all_files = embedded_file('Foo.Bar')
        index = embedded_file('Foo.Bar', 'index.html')

    Extract embedded file from the ``DATA`` section of a class, all files will be
    cached once they have been accessed for the first time. ::

        for content in data_section('Foo.Bar'):
            print(content)
    """
    if filename:
        return _all(modname)[filename]
    else:
        return _all(modname)


def load_module(name):
    """::

        module = load_module('Foo.Bar')

    Load a module and ignore it if it is not found. Note that modules are
    checked for a :func:`new` factory function to see if they are already
    loaded and compatible with :mod:`Pyjo`. ::

        module = load_module('Foo.Bar')
        if not module:
            print('Not found!')
    """
    try:
        module = importlib.import_module(name)
        if hasattr(module, 'new'):
            return module
        else:
            return
    except ImportError:
        return


def _all(modname):
    if modname in CACHE:
        return CACHE[modname]

    module = load_module(modname)
    if not module or not hasattr(module, 'DATA'):
        return {}

    data = module.DATA

    # Split files
    files = re_files.split(data)

    if len(files) < 3:
        return {}

    files.pop(0)

    # Find data
    all_files = CACHE[modname] = {}

    while len(files) >= 2:
        name = files.pop(0)
        content = files.pop(0)
        name, n = re_base64.subn('', name)
        if n:
            all_files[name] = b64_decode(content)
            if modname not in BIN:
                BIN[modname] = {}
            BIN[modname][name] = True
        else:
            all_files[name] = content

    return all_files
