#!/usr/bin/env python

# Usage:
#
#   python test.py
#   PROVE= python test.py
#   python setup.py
#   PYTHONPATH=. nosetests

import os
import subprocess
import sys
import unittest


class TestSuite(unittest.TestSuite):
    def __init__(self, *args, **kwargs):
        super(TestSuite, self).__init__(*args, **kwargs)
        test_loader = unittest.defaultTestLoader
        test_suite = test_loader.discover('t/pyjo', pattern='*.py')
        for t in test_suite:
            self.addTest(t)


def run():
    try:
        prove = os.getenv('PROVE', 'prove')
        args = sys.argv
        if len(args) > 2 and args[0].endswith('setup.py') and args[1] == 'test':
            args = args[2:]
        else:
            args = args[1:]
        if not list(map(lambda a: True if a.startswith('t/') else False, args)).count(True):
            args += ['t/pyjo']
        os.putenv('PYTHONPATH', '.')
        cmd = [prove, '--ext=py', '--exec=' + sys.executable] + args
        subprocess.call(cmd)
    except OSError:
        unittest.main(defaultTest='TestSuite')


if __name__ == '__main__':
    run()
