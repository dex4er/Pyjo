import os
import subprocess
import sys
import unittest


class TestSuite(unittest.TestSuite):
    def run(self, *args, **kwargs):

        # use the default shared TestLoader instance
        test_loader = unittest.defaultTestLoader

        # use the basic test runner that outputs to sys.stderr
        test_runner = unittest.TextTestRunner()

        # automatically discover all tests in the current dir of the form test*.py
        # NOTE: only works for python 2.7 and later
        test_suite = test_loader.discover('t/pyjo', pattern='*.py')

        # run the test suite
        test_runner.run(test_suite)


if __name__ == '__main__':
    try:
        prove = os.getenv('PROVE', 'prove')
        if len(sys.argv) > 1 and sys.argv[1] != '':
            prove_args = sys.argv[1:]
        else:
            prove_args = []
        os.putenv('PYTHONPATH', '.')
        cmd = [prove, '--ext=py', '--exec=' + sys.executable, '--recurse', 't/pyjo'] + prove_args
        subprocess.call(cmd)
    except OSError:
        TestSuite().run()
