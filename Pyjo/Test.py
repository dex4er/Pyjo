"""
Pyjo.Test
"""

from __future__ import print_function, unicode_literals

import os
import re
import subprocess
import sys
import traceback
import unittest


__all__ = ['cmp_ok', 'done_testing', 'diag', 'fail_ok', 'in_ok', 'is_ok',
           'isa_ok', 'is_deeply_ok', 'isnt_ok', 'like_ok', 'none_ok',
           'not_in_ok', 'ok', 'pass_ok', 'plan', 'skip', 'throws_ok',
           'unlike_ok']


done = False
failed = 0
test = 0
tests = 0


def cmp_ok(got, operator, expected, test_name=None):
    if test_name is None:
        test_name = 'An object {0}'.format(type(got))
    test_name = "{0} {1} {2}".format(test_name, operator, repr(expected))
    methods = {
        '==': lambda a, b: a == b,
        '>=': lambda a, b: a >= b,
        '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b,
        '<': lambda a, b: a < b,
        '!=': lambda a, b: a != b,
    }
    check = methods[operator](got, expected)
    _ok(check, test_name)
    if not check:
        diag("    {0}\n        {1}\n    {2}\n".format(repr(got), operator, repr(expected)))


def diag(*args):
    _print('# ' + "\n# ".join(''.join(args).split("\n")), file=sys.stderr)


def done_testing():
    global done, failed, test, tests

    if done:
        fail_ok('done_testing() was already called')
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


def fail_ok(test_name=None):
    _ok(False, test_name)


def in_ok(got, elem, test_name=None):
    if test_name is None:
        test_name = "an object {0}".format(type(got))
    test_name = "{0} is in {1}".format(repr(elem), test_name)
    try:
        check = elem in got
    except TypeError:
        check = False
    _ok(check, test_name)
    if not check:
        diag("         got: {0}".format(repr(got)))


def is_deeply_ok(got, expected, test_name=None):
    test_name = "{0} is {1}".format(test_name, repr(expected))
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


def is_ok(got, expected, test_name=None):
    if test_name is None:
        test_name = 'An object {0}'.format(type(got))
    test_name = "{0} is {1}".format(test_name, repr(expected))
    check = got == expected
    _ok(check, test_name)
    if not check:
        diag("         got: {0}\n    expected: {1}\n".format(repr(got), repr(expected)))


def isa_ok(got, cls, test_name=None):
    if test_name is None:
        test_name = "An object {0}".format(type(got))
    test_name = "{0} is object {1}".format(test_name, cls)
    check = isinstance(got, cls)
    _ok(check, test_name)


def isnt_ok(got, expected, test_name=None):
    if test_name is None:
        test_name = 'An object {0}'.format(type(got))
    test_name = "{0} is {1}".format(test_name, repr(expected))
    check = got != expected
    _ok(check, test_name)
    if not check:
        diag("         got: {0}\n    expected: anything else\n".format(repr(got)))


def like_ok(got, expected, flags='', test_name=None):
    FLAGS = {
        'd': re.DEBUG,
        'i': re.IGNORECASE,
        'l': re.LOCALE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'u': re.UNICODE,
        'x': re.VERBOSE,
    }
    re_flags = 0
    for c in flags:
        re_flags |= FLAGS[c]
    if test_name is None:
        test_name = "An object {0}".format(type(got))
    test_name = "{0} matches {1}".format(test_name, repr(expected))
    try:
        check = re.search(expected, got, re_flags)
    except:
        check = False
    _ok(check, test_name)
    if not check:
        diag("                {0}\n  doesn't match {1}\n".format(repr(got), repr(expected)))


def none_ok(got, test_name=None):
    if test_name is None:
        test_name = "An object {0} is None".format(type(got))
    else:
        test_name = "{0} is None".format(test_name)
    check = got is None
    _ok(check, test_name)


def not_in_ok(got, elem, test_name=None):
    if test_name is None:
        test_name = "an object {0}".format(type(got))
    test_name = "{0} is not in {1}".format(repr(elem), test_name)
    try:
        check = elem not in got
    except TypeError:
        check = False
    _ok(check, test_name)
    if not check:
        diag("         got: {0}".format(repr(got)))


def ok(check, test_name=None):
    _ok(check, test_name)


def pass_ok(test_name=None):
    _ok(True, test_name)


def plan(**kwargs):
    global tests
    if 'tests' in kwargs:
        tests = kwargs['tests']
        _print('1..{0}'.format(tests))


def run(script=__file__, srcdir='.'):
    python_path = os.getenv('PYTHONPATH', '')
    if python_path and python_path != '.':
        python_path = srcdir + ':' + python_path
    else:
        python_path = srcdir
    os.putenv('PYTHONPATH', python_path)
    p = subprocess.Popen([sys.executable, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if p.returncode:
        raise Error(stderr)


def skip(why=None, how_many=1):
    global test
    if why is not None:
        message = "skip " + why
    else:
        message = "skip"
    for _ in range(how_many):
        test += 1
        _print("ok {0} # {1}".format(test, message))


def throws_ok(cb, expected, test_name=None):
    if test_name is None:
        test_name = "Raised {0}".format(expected.__name__)
    else:
        test_name = "{0} raised {1}".format(test_name, expected.__name__)
    got = None
    check = False
    try:
        cb()
    except expected:
        check = True
    except Exception as e:
        got = e
    _ok(check, test_name)
    if not check:
        diag("         got: {0}\n    expected: {1}\n".format(got.__class__.__name__ if got is not None else None, expected.__name__))


def unlike_ok(got, expected, flags='', test_name=None):
    FLAGS = {
        'd': re.DEBUG,
        'i': re.IGNORECASE,
        'l': re.LOCALE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'u': re.UNICODE,
        'x': re.VERBOSE,
    }
    re_flags = 0
    for c in flags:
        re_flags |= FLAGS[c]
    if test_name is None:
        test_name = "An object {0}".format(type(got))
    test_name = "{0} doesn't match {1}".format(test_name, repr(expected))
    try:
        check = not re.search(expected, got, re_flags)
    except:
        check = True
    _ok(check, test_name)
    if not check:
        diag("                {0}\n        matches {1}\n".format(repr(got), repr(expected)))


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
    vnames = ['     ' + re.sub(r'\$FOO', 'got', vname),
              re.sub(r'\$FOO', 'expected', vname)]

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
        if isinstance(test_name, int) or '{0}'.format(test_name).isdigit():
            diag("    You named your test '{0}'.  You shouldn't use numbers for your test names.\n    Very confusing.".format(test_name))
        message += ' - {0}'.format(test_name)

    _print(message)

    if not check:
        if test_name is not None:
            diag("  Failed test '{0}'".format(test_name))
        else:
            diag("  Failed test")
        diag(''.join(traceback.format_stack()[:-2]))


def _print(*args, **kwargs):
    output = kwargs.get('file', sys.stdout)
    string = ' '.join(args) + "\n"
    encoding = sys.stdout.encoding
    if not encoding or encoding.lower() != 'utf-8':
        string = string.encode('ascii', 'backslashreplace').decode('ascii')
    output.write(string)
    output.flush()


class DoesNotExist(object):
    pass


class Error(Exception):
    pass


class Guard(object):
    def __del__(self):
        global failed, done, tests
        if test and not tests and not done:
            print('# Tests were run but no plan was declared and done_testing() was not seen.', file=sys.stderr)

        if not done:
            if not failed:
                failed = 255 - test
            try:
                os._exit(failed)
            except:
                pass

_guard = Guard()


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
