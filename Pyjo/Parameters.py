# -*- coding: utf-8 -*-

"""
Pyjo.Parameters
"""

import Pyjo.Base.String

from Pyjo.Regexp import m, s
from Pyjo.Util import b, isiterable_not_str, lazy, u, url_escape, url_unescape


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

    charset = 'utf-8'
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
        new_obj.charset = self.charset
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

            charset = self.charset

            for pair in string.split('&'):
                g = pair == m(r'^([^=]+)(?:=(.*))?$')

                if not g:
                    continue

                name = g[1]
                value = g[2] if g[2] is not None else ''

                # Replace "+" with whitespace, unescape and decode
                name -= s(r'\+', ' ', 'g')
                value -= s(r'\+', ' ', 'g')

                name = url_unescape(name)
                value = url_unescape(value)

                if charset:
                    name = b(name).decode(charset)
                    value = b(value).decode(charset)

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

        # String
        charset = self.charset
        if self._string is not None:
            if charset:
                string = self._string.encode(charset).decode('iso-8859-1')
            else:
                string = self._string
            return url_escape(string, r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@/?')

        # Build pairs
        params = self.params
        if not params:
            return ''

        pairs = []
        for name, value in list(zip(params[::2], params[1::2])):
            name = u(name)
            value = u(value)

            if charset:
                name = name.encode(charset).decode('iso-8859-1')
                value = value.encode(charset).decode('iso-8859-1')

            name = url_escape(name, r'^A-Za-z0-9\-._~!$\'()*,:@/?')
            value = url_escape(value, r'^A-Za-z0-9\-._~!$\'()*,:@/?')

            name -= s(r'%20', '+', 'g')
            value -= s(r'%20', '+', 'g')

            pairs.append(name + '=' + value)

        return '&'.join(pairs)

    def _param(self, name):
        values = []
        params = self.params
        for k, v in list(zip(params[::2], params[1::2])):
            if k == name:
                values.append(v)

        return values

    def __iter__(self):
        params = self.params
        for p in params:
            yield p

    def __bool__(self):
        return True


new = Pyjo_Parameters.new
object = Pyjo_Parameters  # @ReservedAssignment
