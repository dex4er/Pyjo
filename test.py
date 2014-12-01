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
        if len(args) > 1 and args[0].endswith('setup.py'):
            if len(args) > 2 and args[1] == 'test':
                prove_args = args[2:]
            else:
                prove_args = []
        elif len(args) > 1 and args[1] != '':
            prove_args = args[1:]
        else:
            prove_args = []
        os.putenv('PYTHONPATH', '.')
        cmd = [prove, '--ext=py', '--exec=' + sys.executable, 't/pyjo'] + prove_args
        subprocess.call(cmd)
    except OSError:
        unittest.main(defaultTest='TestSuite')


if __name__ == '__main__':
    run()
