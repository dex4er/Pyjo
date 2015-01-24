"""
Pyjo.Regexp
"""


import importlib
import os


try:
    re = importlib.import_module(os.environ.get('PYJO_REGEXP', 'regex'))
except ImportError:
    import re


re_EXTRA = 0

FLAGS = {
    'c': re_EXTRA,
    'd': re.DEBUG,
    'g': re_EXTRA,
    'i': re.IGNORECASE,
    'l': re.LOCALE,
    'm': re.MULTILINE,
    'o': re_EXTRA,
    'r': re_EXTRA,
    's': re.DOTALL,
    'u': re.UNICODE,
    'x': re.VERBOSE,
}


CACHE = {}


class Pyjo_Regexp(object):

    def __init__(self, action, pattern, replacement=None, flags='', pos=0):
        self._action = action
        self._pattern = pattern
        self._replacement = replacement
        self._flags = flags
        self._re = re.compile(pattern, self._re_flags(flags))
        self.pos = pos

    @classmethod
    def m(cls, pattern, flags=''):
        idx = '\0'.join((str(hash(pattern)), str(hash(flags)),))
        if idx in CACHE:
            return CACHE[idx]
        new_obj = cls('m', pattern, flags=flags)
        if 'o' not in flags:
            CACHE[idx] = new_obj
        return new_obj

    @classmethod
    def s(cls, pattern, replacement, flags=''):
        idx = '\0'.join((str(hash(pattern)), str(hash(replacement)), str(hash(flags)),))
        if idx in CACHE:
            return CACHE[idx]
        new_obj = cls('s', pattern, replacement, flags=flags)
        if 'o' not in flags:
            CACHE[idx] = new_obj
        return new_obj

    def clone(self):
        new_obj = type(self)(self._action, self._pattern, replacement=self._replacement, flags=self._flags)
        return new_obj

    def _re_flags(self, str_flags=''):
        flags = 0
        for f in str_flags:
            if f in FLAGS:
                flags |= FLAGS[f]
            else:
                raise ValueError('Bad flag: {0}'.format(f))
        return flags

    def _match_result(self, match):
        result = {}
        if match is not None:
            result[0] = match.group()
            if 'c' in self._flags:
                result['start'] = match.start()
                result['end'] = match.end()
            result.update(enumerate(match.groups(), start=1))
            result.update(match.groupdict())
        return result

    def _match_iter(self, string):
        matchiter = self._re.finditer(string, self.pos)
        if matchiter is None:
            return
        for match in matchiter:
            yield self._match_result(match)
        return

    def match(self, string, _flag_g=None, _flag_r=None):
        if _flag_g is None:
            _flag_g = 'g' in self._flags

        if self._action == 'm':
            if _flag_g:
                return self._match_iter(string)
            else:
                match = self._re.search(string, self.pos)
                return self._match_result(match)

        elif self._action == 's':
            if _flag_g:
                count = 0
            else:
                count = 1

            if callable(self._replacement):
                replacement = lambda m: self._replacement(self._match_result(m))
            else:
                replacement = self._replacement

            if _flag_r is None:
                _flag_r = 'r' in self._flags

            if _flag_r:
                new_string = self._re.sub(replacement, string, count=count)
                return new_string
            else:
                match = self._re.search(string)
                result = self._match_result(match)
                (new_string, count) = self._re.subn(replacement, string, count=count)
                if _flag_g:
                    return (new_string, result, count)
                else:
                    return (new_string, result)

    def __eq__(self, other):
        return self.match(other)

    def __ne__(self, other):
        return not self.match(other)

    def __rsub__(self, other):
        return self.match(other, _flag_r=True)

    def __rmul__(self, other):
        while True:
            (other, replaced) = self.match(other, _flag_g=False, _flag_r=False)
            if not replaced:
                break
        return other

    def __call__(self, string):
        return self.match(string)

    def __repr__(self):
        if self._action == 'm':
            return "regexp.m({0}, {1})".format(repr(self._pattern), repr(self._flags))
        elif self._action == 's':
            return "regexp.s({0}, {1}, {2})".format(repr(self._pattern), repr(self._replacement), repr(self._flags))
        else:
            return super(Pyjo_Regexp, self).__repr__()


regexp = Pyjo_Regexp
m = regexp.m
s = regexp.s

object = Pyjo_Regexp  # @ReservedAssignment
