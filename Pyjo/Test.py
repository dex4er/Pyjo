"""
Pyjo.Test
"""

from __future__ import print_function

import os
import re
import subprocess
import sys
import traceback
import unittest
from _codecs_cn import __file__


__all__ = ['done_testing', 'diag', 'fail', 'is_ok', 'isa_ok', 'is_deeply_ok',
           'none_ok', 'ok', 'pass_ok', 'plan']


test = 0

tests = 0
failed = 0

done = False


def _print(*args, **kwargs):
    output = kwargs.get('file', sys.stdout)
    print(*args, file=output)
    output.flush()


def diag(*args):
    _print('# ' + "\n# ".join(''.join(args).split("\n")), file=sys.stderr)


def _ok(check, test_name=None):
    global failed, test

    test += 1

    if not check:
        message = 'not '
        failed += 1
    else:
        message = ''

    message += 'ok {0}'.format(test)

    if test_name is not None:
        if isinstance(test_name, int) or str(test_name).isdigit():
            diag("    You named your test '{0}'.  You shouldn't use numbers for your test names.\n    Very confusing.".format(test_name))
        message += ' - {0}'.format(test_name)

    _print(message)

    if not check:
        if test_name is not None:
            diag("  Failed test '{0}'".format(test_name))
        else:
            diag("  Failed test")
        diag(''.join(traceback.format_stack()[:-2]))


def ok(check, test_name=None):
    _ok(check, test_name)


def pass_ok(test_name=None):
    _ok(True, test_name)


def fail(test_name=None):
    _ok(False, test_name)


def is_ok(got, expected, test_name=None):
    if test_name is None:
        test_name = 'An object {0}'.format(type(got))
    test_name = "{0} is {1}".format(test_name, repr(expected))
    check = got == expected
    _ok(check, test_name)
    if not check:
        diag("         got: {0}\n    expected: {1}".format(repr(got), repr(expected)))


def isa_ok(got, cls, test_name=None):
    if test_name is None:
        test_name = "An object {0}".format(type(got))
    test_name = "{0} is object {1}".format(test_name, cls)
    check = isinstance(got, cls)
    _ok(check, test_name)


def none_ok(got, test_name=None):
    if test_name is None:
        test_name = "An object {0} is None".format(type(got))
    else:
        test_name = "{0} is None".format(test_name)
    check = got is None
    _ok(check, test_name)


def is_deeply_ok(got, expected, test_name=None):
    if isinstance(got, (list, tuple, set, dict)) and isinstance(expected, (list, tuple, set, dict)):
        stack = []
        check = _deep_check(stack, got, expected)
        _ok(check, test_name)
        if not check:
            diag(_format_stack(stack))
    else:
        check = got == expected
        _ok(check, test_name)
        if not check:
            diag("         got: {0}\n    expected: {1}".format(repr(got), repr(expected)))


def plan(**kwargs):
    global tests
    if 'tests' in kwargs:
        tests = kwargs['tests']
        _print('1..{0}'.format(tests))


def done_testing():
    global done, failed, test, tests

    if done:
        fail('done_testing() was already called')
        return

    if not tests:
        tests = test
        _print('1..{0}'.format(tests))

    if not tests:
        diag('No tests run!')
        failed = 255

    if failed:
        sys.exit(failed)

    done = True


def _eq_array(stack, t, a1, a2):
    if a1 == a2:
        return True

    check = True
    for i in range(max(len(a1), len(a2))):
        if i < len(a1):
            e1 = a1[i]
        else:
            e1 = DoesNotExist

        if i < len(a2):
            e2 = a2[i]
        else:
            e2 = DoesNotExist

        stack.append({'type': t, 'idx': i, 'vals': [e1, e2]})
        check = _deep_check(stack, e1, e2)
        if check:
            stack.pop()
        else:
            break

    return check


def _eq_hash(stack, t, h1, h2):
    if h1 == h2:
        return True

    check = True
    if len(h1) > len(h2):
        bigger = h1
    else:
        bigger = h2

    for k in sorted(bigger):
        if k in h1:
            e1 = h1[k]
        else:
            e1 = DoesNotExist

        if k in h2:
            e2 = h2[k]
        else:
            e2 = DoesNotExist

        stack.append({'type': t, 'idx': k, 'vals': [e1, e2]})
        check = _deep_check(stack, e1, e2)
        if check:
            stack.pop()
        else:
            break

    return check


def _deep_check(stack, e1, e2):
        if e1 is None or e2 is None:
            if e1 is None and e2 is None:
                return True
            else:
                stack.append({'vals': [e1, e2]})
                return False

        if id(e1) == id(e2):
            return True

        if e1 == e2:
            return True

        if isinstance(e1, list) and isinstance(e2, list):
            return _eq_array(stack, 'list', e1, e2)

        if isinstance(e1, tuple) and isinstance(e2, tuple):
            return _eq_array(stack, 'tuple', e1, e2)

        if isinstance(e1, set) and isinstance(e2, set):
            return _eq_array(stack, 'set', sorted(e1), sorted(e2))

        if isinstance(e1, dict) and isinstance(e2, dict):
            return _eq_hash(stack, 'dict', e1, e2)

        stack.append({'vals': [e1, e2]})
        return False


re_foo = re.compile(r'\$FOO')
re_indent = re.compile(r'^', re.M)


def _format_stack(stack):
    vname = '$FOO'

    for entry in stack:
        t = entry.get('type', '')
        idx = entry.get('idx', 0)
        if t == 'list' or t == 'tuple' or t == 'dict':
            vname += '[{0}]'.format(idx)
        elif t == 'set':
            vname = 'sorted({0})[{1}]'.format(vname, idx)

    vals = stack[-1]['vals']
    vnames = ['     ' + re_foo.sub('got', vname),
              re_foo.sub('expected', vname)]

    out = "Structures begin differing at:\n"
    for idx in range(len(vals)):
        val = vals[idx]
        if val is None:
            val = 'None'
        elif val is DoesNotExist:
            val = 'Does not exist'
        else:
            val = repr(val)
        vals[idx] = val

    out += "{0} = {1}\n".format(vnames[0], vals[0])
    out += "{0} = {1}\n".format(vnames[1], vals[1])

    out = '    ' + "\n    ".join(out.split("\n"))

    return out


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


class DoesNotExist(object):
    pass


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
