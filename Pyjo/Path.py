"""
Pyjo.Path
"""

import Pyjo.Base.String

from Pyjo.Util import url_escape


class Pyjo_Path(Pyjo.Base.String.object):

    charset = 'utf-8'
    leading_slash = None
    parts = []
    trailing_slash = None
    _path = None

    def __init__(self, path=None):
        super(Pyjo_Path, self).__init__()
        if path is not None:
            self.parse(path)

    def parse(self, path):
        self._path = path
        self.leading_slash = None
        self.parts = []
        self.trailing_slash = None
        return self

    def to_str(self):
        # Path
        charset = self.charset
        if self._path is not None:
            if charset:
                path = self._path.encode(charset).decode('iso-8859-1')
            else:
                path = self._path
            return url_escape(path, r'^A-Za-z0-9\-._~!$&\'()*+,;=%:@/')

        # TODO Build path
        return


new = Pyjo_Path.new
object = Pyjo_Path  # @ReservedAssignment
