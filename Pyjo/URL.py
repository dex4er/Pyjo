"""
Pyjo.URL
"""

import re

from Pyjo.Base import *
from Pyjo.Parameters import *
from Pyjo.Path import *

from Pyjo.Base import accessor, Omitted
from Pyjo.Util import url_escape


__all__ = ['Pyjo_URL']


re_url = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')
re_userinfo = re.compile(r'^([^\@]+)\@')
re_port = re.compile(r':(\d+)$')
re_ihost = re.compile(r'[^\x00-\x7f]')
re_path = re.compile(r'^[/?]')


class Pyjo_URL(Pyjo_Base):

    def __init__(self, url=None):
        self.base = None
        self.fragment = None
        self.host = None
        self.port = None
        self.scheme = None
        self.userinfo = None

        self._path = None
        self._query = None

        if url is not None:
            self.parse(url)

    def parse(self, url):
        m = re_url.match(url)
        self.set(scheme=m.group(2), authority=m.group(4), path=m.group(5),
                 query=m.group(7), fragment=m.group(9))
        return self

    @accessor
    def authority(self, authority=Omitted):
        if authority is not Omitted:
            if authority is None:
                return self

            # Userinfo
            m = re_userinfo.search(authority)
            if m:
                self.userinfo = m.group(1)
                # TODO url_unescape
                authority = re_userinfo.sub('', authority)

            # Port
            m = re_port.search(authority)
            if m:
                self.port = m.group(1)
                authority = re_port.sub('', authority)

            # Host
            self.host = authority
            return self

        else:
            # Build authority
            authority = self.host_port()
            if authority is None:
                return

            info = self.userinfo
            if info is None:
                return authority

            return url_escape(info, '^A-Za-z0-9\-._~!$&\'()*+,;=:') + '@' + authority

    def host_port(self):
        host = self.host
        port = self.port
        if port is not None:
            return '{0}:{1}'.format(host, port)
        else:
            return host

    @accessor
    def path(self, value=Omitted):
        if value is Omitted:
            if self._path is None:
                self._path = Pyjo_Path()
            return self._path
        else:
            # TODO old path / new path
            self._path = Pyjo_Path(value)
            return self

    def path_query(self):
        query = self.query.to_string()
        if len(query):
            query = '?' + query
        else:
            query = ''
        return self.path.to_string() + query;

    def protocol(self):
        scheme = self.scheme

        if scheme is None:
            return ''

        return scheme.lower()

    @accessor
    def query(self, value=Omitted):
        if value is Omitted:
            if self._query is None:
                self._query = Pyjo_Parameters()
            return self._query
        else:
            self._query = Pyjo_Parameters(value)
            return self

    def to_string(self):
        # Scheme
        url = ''
        proto = self.protocol()

        if proto:
            url += proto + ':'

        # Authority
        authority = self.authority

        if authority is not None:
            url += '//' + authority

        # Path and query
        path = self.path_query()

        if not authority or path == '' or re_path.search(path):
            url += path
        else:
            url += '/' + path

        # Fragment
        fragment = self.fragment

        if fragment is None:
            return url

        return url + '#' + url_escape(fragment, r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@/?')

    __str__ = to_string
