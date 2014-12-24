# -*- coding: utf-8 -*-

"""
Pyjo.Parameters
"""

import Pyjo.Base.String

from Pyjo.Regexp import m, s
from Pyjo.Util import isiterable_not_str, lazy, u, url_escape, url_unescape


class Pyjo_Parameters(Pyjo.Base.String.object):
    """
    .. code-block:: python

        import Pyjo.Parameters

        # Parse
        params = Pyjo.Parameters.new('foo=bar&baz=23')
        print(params.param('baz'))

        # Build
        params = Pyjo.Parameters.new(foo='bar', baz=23)
        params.append(i='♥ Pyjo')
        print(params)

    :class:`Pyjo.Parameters.object` is a container for form parameters used by :class:`Pyjo.URL.object`
    and based on `RFC 3986 <http://tools.ietf.org/html/rfc3986>`_ as well as `the
    HTML Living Standard <https://html.spec.whatwg.org>`_.
    """

    _charset = 'utf8'
    _params = lazy(lambda self: [])
    _string = None

    def append(self, *args, **kwargs):
        """
        .. code-block:: python

           params = params.append(foo='ba&r')
           params = params.append(foo=['ba&r', 'baz'])
           params = params.append(foo=['bar', 'baz'], bar => 23)

        Append parameters. Note that this method will normalize the parameters.

        .. code-block:: python

           # "foo=bar&foo=baz"
           Pyjo.Parameters.new('foo=bar').append(foo='baz')

           # "foo=bar&foo=baz&foo=yada"
           Pyjo.Parameters.new('foo=bar').append(foo=['baz', 'yada'])

           # "foo=bar&foo=baz&foo=yada&bar=23"
           Pyjo.Parameters.new('foo=bar').append(foo=['baz', 'yada'], bar=23)

        :param args: one parameters as key/value pair of args
        :param kwargs: one parameter as kwargs
        :rtype: self
        """

        params = self._params
        for p in list(zip(args[::2], args[1::2])) + sorted(kwargs.items()):
            (k, v) = p
            if isiterable_not_str(v):
                for vv in v:
                    params.append(k)
                    params.append(vv)
            else:
                params.append(k)
                params.append(v)
        return self

    def clone(self):
        new_obj = type(self)()
        new_obj._charset = self._charset
        if self._string is not None:
            new_obj._string = self._string
        else:
            new_obj._params = list(self._params)
        return new_obj

    def every_param(self, name):
        return self._param(name)

    def merge(self, *args):
        for p in args:
            self.params += p.params

    def __init__(self, *args, **kwargs):
        super(Pyjo_Parameters, self).__init__()
        self.parse(*args, **kwargs)

    def param(self, name=None, value=None, **kwargs):
        # List names
        if not name and not kwargs:
            return sorted(self.to_dict().keys())

        # Multiple names
        if name is not None and isinstance(name, (list, tuple,)):
            return [self.param(n) for n in name]

        # Last value
        if value is None and not kwargs:
            param = self._param(name)
            if param:
                return self._param(name)[-1]
            else:
                return

        # Replace values
        self.remove(name)
        if not kwargs:
            return self.append(name, value)
        else:
            return self.append(**kwargs)

    @property
    def params(self):
        # Parse string
        if self._string is not None:
            string = self._string
            self._string = None
            self._params = []

            if not len(string):
                return self._params

            charset = self._charset

            for pair in string.split('&'):
                g = pair == m(r'^([^=]+)(?:=(.*))?$')
                if not g:
                    continue
                name, value = g[1], g[2] if g[2] is not None else ''

                # Replace "+" with whitespace, unescape and decode
                name -= s(r'\+', ' ', 'g')
                value -= s(r'\+', ' ', 'g')

                name = url_unescape(name)
                value = url_unescape(value)

                if charset:
                    name = u(name).decode(charset)
                    value = u(value).decode(charset)

                self._params.append(name)
                self._params.append(value)

        return self._params

    @params.setter
    def params(self, value=None):
        # Replace parameters
        self._params = value
        self._string = None
        return self

    def parse(self, *args, **kwargs):
        if len(args) > 1 or kwargs:
            # Pairs
            return self.append(*args, **kwargs)
        else:
            if args:
                # String
                self._string = args[0]
            return self

    def remove(self, name):
        params = self.params
        i = 0
        while i < len(params):
            if params[i] == name:
                params.pop(i)
                params.pop(i)
            else:
                i += 2
        return self

    def to_dict(self):
        d = {}
        params = self.params
        for k, v in list(zip(params[::2], params[1::2])):
            if k in d:
                if not isinstance(d[k], list):
                    d[k] = [d[k]]
                else:
                    d[k].append(v)
            else:
                d[k] = v
        return d

    def to_string(self):
        if self._string is not None:
            return self._string
        elif self._params and len(self._params):
            return '&'.join([url_escape(str(p[0])) + '=' + url_escape(str(p[1])) for p in list(zip(self._params[::2], self._params[1::2]))])
        else:
            return ''

    def _param(self, name):
        values = []
        params = self._params
        for k, v in list(zip(params[::2], params[1::2])):
            if k == name:
                values.append(v)

        return values


new = Pyjo_Parameters.new
object = Pyjo_Parameters  # @ReservedAssignment
