import Pyjo.Test


class NoseTest(Pyjo.Test.NoseTest):
    script = __file__
    srcdir = '../..'


class UnitTest(Pyjo.Test.UnitTest):
    script = __file__


if __name__ == '__main__':

    from Pyjo.Test import *  # @UnusedWildImport

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
