import os
import subprocess
import sys
import unittest


class Test(unittest.TestCase):
    def test_pyjo_url(self):
        os.putenv('PYTHONPATH', '.')
        subprocess.check_output([sys.executable, __file__])


if __name__ == '__main__':

    from Pyjo.Test import *

    from Pyjo.URL import *

    # Simple
    url = Pyjo_URL('HtTp://Example.Com')
    is_ok(url.scheme,    'HtTp',        'right scheme')
    is_ok(url.protocol,  'http',        'right protocol')
    is_ok(url.host,      'Example.Com', 'right host')
    is_ok(url.ihost,     'example.com', 'right internationalized host')
    is_ok(url.authority, 'example.com', 'right authority')
    is_ok(str(url), 'http://example.com', 'right format')

    done_testing()
