"""
Pyjo.Parameters
"""

import Pyjo.Base.String

from Pyjo.Util import isiterable, lazy, url_escape


# TODO stub
class Pyjo_Parameters(Pyjo.Base.String.object):

    charset = 'UTF-8'

    _params = lazy(lambda self: [])
    _string = None

    def append(self, *args, **kwargs):
        params = self._params
        for p in list(zip(args[::2], args[1::2])) + sorted(kwargs.items()):
            (k, v) = p
            if isiterable(v):
                for vv in v:
                    params.append(k)
                    params.append(vv)
            else:
                params.append(k)
                params.append(v)
        return self

    def __init__(self, *args, **kwargs):
        super(Pyjo_Parameters, self).__init__()
        self.parse(*args, **kwargs)

    def parse(self, *args, **kwargs):
        if len(args) > 1 or kwargs:
            # Pairs
            return self.append(*args, **kwargs)
        else:
            # String
            self._string = args[0]
            return self

    def to_string(self):
        if self._string is not None:
            return self._string
        elif self._params:
            return '&'.join([url_escape(str(p[0])) + '=' + url_escape(str(p[1])) for p in list(zip(self._params[::2], self._params[1::2]))])
        else:
            return ''


new = Pyjo_Parameters.new
object = Pyjo_Parameters  # @ReservedAssignment
