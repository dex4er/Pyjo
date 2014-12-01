"""
Pyjo.Test
"""

from __future__ import print_function

import os
import subprocess
import sys
import traceback
import unittest
from _codecs_cn import __file__


__all__ = ['done_testing', 'diag', 'fail', 'is_ok', 'ok', 'pass_ok']


test = 0

tests = 0
failed = 0

done = False


def diag(*args):
    print('# ' + "\n# ".join(''.join(args).split("\n")), file=sys.stderr)


def _ok(status, test_name=None):
    global failed, test

    test += 1

    if not status:
        message = 'not '
        failed += 1
    else:
        message = ''

    message += 'ok {0}'.format(test)

    if test_name is not None:
        if isinstance(test_name, int) or test_name.isdigit():
            diag("    You named your test '{0}'.  You shouldn't use numbers for your test names.\n    Very confusing.".format(test_name))
        message += ' - {0}'.format(test_name)

    print(message)

    if not status:
        diag(''.join(traceback.format_stack()[:-2]))


def ok(status, test_name=None):
    _ok(status, test_name)


def pass_ok(test_name=None):
    _ok(True, test_name)


def fail(test_name=None):
    _ok(False, test_name)


def is_ok(got, expected, test_name=None):
    status = got == expected
    _ok(status, test_name)
    if not status:
        diag("         got: '{0}'\n    expected: '{1}'".format(got, expected))

def done_testing():
    global done, failed, test, tests

    if done:
        fail('done_testing() was already called')
        return

    if not tests:
        tests = test

    print('1..{0}'.format(tests))

    if not tests:
        diag('No tests run!')
        failed = 255

    if failed:
        sys.exit(failed)

    done = True


class Guard(object):
    def __del__(self):
        global failed, done, tests
        if test and not tests and not done:
            diag('Tests were run but no plan was declared and done_testing() was not seen.')

        if not done:
            if not failed:
                failed = 255 - test
            os._exit(failed)

_guard = Guard()


def run(script=__file__, srcdir='.'):
    python_path = os.getenv('PYTHONPATH', '')
    if python_path and python_path != '.':
        python_path = srcdir + ':' + python_path
    else:
        python_path = srcdir
    os.putenv('PYTHONPATH', python_path)
    subprocess.check_output([sys.executable, script])


class NoseTest(object):
    script = __file__
    srcdir = '.'

    def test_nose(self):
        run(self.script, self.srcdir)


class UnitTest(unittest.TestCase):
    script = __file__
    srcdir = '.'

    def test_unit(self):
        run(self.script, self.srcdir)
