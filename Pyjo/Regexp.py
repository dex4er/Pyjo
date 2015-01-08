"""
Pyjo.Regexp
"""


import regex


re_EXTRA = 0

FLAGS = {
    'd': regex.DEBUG,
    'g': re_EXTRA,
    'i': regex.IGNORECASE,
    'l': regex.LOCALE,
    'm': regex.MULTILINE,
    'o': re_EXTRA,
    'r': re_EXTRA,
    's': regex.DOTALL,
    'u': regex.UNICODE,
    'x': regex.VERBOSE,
}


CACHE = {}


class Pyjo_Regexp(object):

    def __init__(self, action, pattern, replacement=None, flags=''):
        self._action = action
        self._pattern = pattern
        self._replacement = replacement
        self._flags = flags
        self._re = regex.compile(pattern, self._re_flags(flags))

    @classmethod
    def m(cls, pattern, flags=''):
        idx = '\0'.join((str(pattern), str(flags),))
        if idx in CACHE:
            return CACHE[idx]
        new_obj = cls('m', pattern, flags=flags)
        if 'o' not in flags:
            CACHE[idx] = new_obj
        return new_obj

    @classmethod
    def s(cls, pattern, replacement, flags=''):
        idx = '\0'.join((str(pattern), str(replacement), str(flags),))
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
            result.update(enumerate(match.groups(), start=1))
            result.update(match.groupdict())
        return result

    def _match_result_iter(self, string):
        for match in self._re.finditer(string):
            yield self._match_result(match)
        return

    def match(self, string, _flag_g=None, _flag_r=None):
        if _flag_g is None:
            _flag_g = 'g' in self._flags

        if self._action == 'm':
            if _flag_g:
                match = self._re.finditer(string)
                return self._match_result_iter(match)
            else:
                match = self._re.search(string)
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
                return (new_string, count, result)

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
