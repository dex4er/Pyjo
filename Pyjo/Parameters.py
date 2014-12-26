# -*- coding: utf-8 -*-

"""
Pyjo.Parameters - Parameters ::

    import Pyjo.Parameters

    # Parse
    params = Pyjo.Parameters.new('foo=bar&baz=23')
    print(params.param('baz'))

    # Build
    params = Pyjo.Parameters.new(foo='bar', baz=23)
    params.append(i='♥ Pyjo')
    print(params)

:class:`Pyjo.Parameters` is a container for form parameters used by :class:`Pyjo.URL`
and based on :rfc:`3986` as well as `the HTML Living Standard <https://html.spec.whatwg.org>`_.
"""

import Pyjo.Base.String

from Pyjo.Regexp import m, s
from Pyjo.Util import isiterable_not_str, lazy, u, url_escape, url_unescape


class Pyjo_Parameters(Pyjo.Base.String.object):
    """::

        params = Pyjo.Parameters.new()
        params = Pyjo.Parameters.new('foo=b%3Bar&baz=23')
        params = Pyjo.Parameters.new(foo='b&ar')
        params = Pyjo.Parameters.new(foo=['ba&r', 'baz'])
        params = Pyjo.Parameters.new(foo=['bar', 'baz'], bar=23)

    Construct a new :class:`Pyjo.Parameters` object and :meth:`parse` parameters if
    necessary.
    """

    charset = 'utf-8'
    """::

        charset = params.charset
        params.charset = 'utf-8'

    Charset used for encoding and decoding parameters, defaults to ``utf-8``. ::

        # Disable encoding and decoding
        params.charset = None
    """

    _params = lazy(lambda self: [])
    _string = None

    def __init__(self, *args, **kwargs):
        super(Pyjo_Parameters, self).__init__()
        self.parse(*args, **kwargs)

    def __iter__(self):
        """::
            for p in params:
                print(p)

            Iterator based on :meth:`params`. Note that this will normalize the parameters.
        """
        params = self.params
        for p in params:
            yield p

    def __bool__(self):
        """::
            b = bool(params)

            Always true.
        """
        return True

    def append(self, *args, **kwargs):
        """::

            params = params.append(foo='ba&r')
            params = params.append(foo=['ba&r', 'baz'])
            params = params.append('foo', ['bar', 'baz'], 'bar', 23)

        Append parameters. Note that this method will normalize the parameters.

        ::

            # "foo=bar&foo=baz"
            Pyjo.Parameters.new('foo=bar').append(foo='baz')

            # "foo=bar&foo=baz&foo=yada"
            Pyjo.Parameters.new('foo=bar').append(foo=['baz', 'yada'])

            # "foo=bar&foo=baz&foo=yada&bar=23"
            Pyjo.Parameters.new('foo=bar').append('foo', ['baz', 'yada'], 'bar', 23)
        """
        params = self.params
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
        """::

            params2 = params.clone()

        Clone parameters.
        """
        new_obj = type(self)()
        new_obj.charset = self.charset
        if self._string is not None:
            new_obj._string = self._string
        else:
            new_obj._params = list(self._params)
        return new_obj

    def every_param(self, name):
        """::

            values = params.every_param('foo')

        Similar to :meth:`param`, but returns all values sharing the same name as a
        list. Note that this method will normalize the parameters. ::

            # Get first value
            print(params.every_param('foo')[0])
        """
        return self._param(name)

    def merge(self, *args):
        """::

            params = params.merge(Pyjo.Parameters.new('foo', 'b&ar', 'baz', 23))

        Merge :class:`Pyjo.Parameters` objects. Note that this method will normalize the
        parameters. ::

            # "foo=bar&foo=baz"
            Pyjo.Parameters.new('foo=bar').merge(Pyjo.Parameters.new('foo=baz'))
        """
        for p in args:
            self.params += p.params

    def param(self, name=None, value=None):
        """::

            names = params.param()
            value = params.param('foo')
            foo, baz = params.param(['foo', 'baz'])
            params = params.param('foo', 'ba&r')
            params = params.param('foo', ['ba;r', 'baz'])

        Access parameter values. If there are multiple values sharing the same name,
        and you want to access more than just the last one, you can use
        :meth:`every_param`. Note that this method will normalize the parameters.
        """
        # List names
        if not name:
            return sorted(self.to_dict().keys())

        # Multiple names
        if name is not None and isinstance(name, (list, tuple,)):
            return [self.param(n) for n in name]

        # Last value
        if value is None:
            param = self._param(name)
            if param:
                return self._param(name)[-1]
            else:
                return

        # Replace values
        self.remove(name)
        return self.append(name, value)

    @property
    def params(self):
        """::

            array = params.params
            params.params = ['foo', 'b&ar', 'baz', 23]

        Parsed parameters. Note that setting this property will normalize the parameters.
        """
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
                    name = name.decode(charset)
                    value = value.decode(charset)

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
        """::

            params = params.parse('foo=b%3Bar&baz=23')

        Parse parameters.
        """
        if len(args) > 1 or kwargs:
            # Pairs
            return self.append(*args, **kwargs)
        else:
            if args:
                # String
                self._string = args[0]
            return self

    def remove(self, name):
        """::

            params = params.remove('foo')

        Remove parameters. Note that this method will normalize the parameters. ::

            # "bar=yada"
            Pyjo.Parameters.new('foo=bar&foo=baz&bar=yada').remove('foo')
        """
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
        """::
            d = params.to_dict()

        Turn parameters into a :class:`dict`. Note that this method will normalize
        the parameters. ::

            # "baz"
            Pyjo.Parameters.new('foo=bar&foo=baz').to_dict()['foo'][1]
        """
        d = {}
        params = self.params
        for k, v in list(zip(params[::2], params[1::2])):
            if k in d:
                if not isinstance(d[k], list):
                    d[k] = [d[k]]
                d[k].append(v)
            else:
                d[k] = v
        return d

    def to_str(self):
        """::

            string = params.to_str()

        Turn parameters into a string.
        """
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

new = Pyjo_Parameters.new
object = Pyjo_Parameters  # @ReservedAssignment
