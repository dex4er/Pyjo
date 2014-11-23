"""
Pyjo.URL
"""

import re

from Pyjo.Base import *


__all__ = ['Pyjo_URL']


re_url = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?')
re_userinfo = re.compile(r'^([^\@]+)\@')
re_port = re.compile(r':(\d+)$')
re_ihost = re.compile(r'[^\x00-\x7f]')


class Pyjo_URL(Pyjo_Base):
    base = None
    fragment = None
    host = None
    port = None
    scheme = None
    userinfo = None

    def __init__(self, url=None):
        if url is not None:
            self.parse(url)

    def parse(self, url):
        m = re_url.match(url)
        (self.scheme, self.authority, self.path, self.query, self.fragment) = \
            m.group(2, 4, 5, 7, 9)
        return self

    @property
    def authority(self):
        return self.host_port

    @authority.setter
    def authority(self, value):
        if value is None:
            return

        # Userinfo
        m = re_userinfo.search(value)
        if m:
            self.userinfo = m.group(1)
            # TODO url_unescape
            value = re_userinfo.sub('', value)

        # Port
        m = re_port.search(value)
        if m:
            self.port = m.group(1)
            value = re_port.sub('', value)

        # Host
        self.host = value
        return self

    @property
    def host_port(self):
        host = self.host
        port = self.port
        if port is not None:
            return '{0}:{1}'.format(host, port)
        else:
            return host
