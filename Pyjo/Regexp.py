"""
Pyjo.Regexp
"""


import re


re_EXTRA = 0

FLAGS = {
    'd': re.DEBUG,
    'g': re_EXTRA,
    'i': re.IGNORECASE,
    'l': re.LOCALE,
    'm': re.MULTILINE,
    'o': re_EXTRA,
    's': re.DOTALL,
    'u': re.UNICODE,
    'x': re.VERBOSE,
}


CACHE = {}


class Pyjo_Regexp(object):

    def __init__(self, action, pattern, replacement='', flags=''):
        self.action = action
        self.pattern = pattern
        self.replacement = replacement
        self.flags = flags
        self.re_flags = self._re_flags(self.flags)
        self.re = re.compile(self.pattern, self.re_flags)

    @classmethod
    def new(cls, regexp):
        if regexp in CACHE:
            return CACHE[regexp]
        params = regexp.split('/')
        if params[0] == 's':
            (pattern, replacement, flags) = params[1:4]
            r = cls('s', pattern, replacement=replacement, flags=flags)
            if 'o' not in flags:
                CACHE[regexp] = r
            return r
        elif params[0] in 'm/':
            (pattern, flags) = params[1:3]
            r = cls('m', pattern, flags=flags)
            if 'o' not in flags:
                CACHE[regexp] = r
            return r
        else:
            raise ValueError('Bad action: {0}'.format(regexp[0]))

    def _re_flags(self, str_flags=''):
        flags = 0
        for f in str_flags:
            if f in FLAGS:
                flags |= FLAGS[f]
            else:
                raise ValueError('Bad flag: {0}'.format(f))
        return flags

    def match(self, string):
        if self.action == 'm':
            if 'g' in self.flags:
                return self.re.findall(string)
            result = {}
            match = self.re.search(string)
            if match is not None:
                result[0] = match.group()
                result.update(enumerate(match.groups(), start=1))
                result.update(match.groupdict())
            return result
        elif self.action == 's':
            return self.re.sub(self.replacement, string, self.re_flags)

    def __eq__(self, other):
        return self.match(other)

    def __isub__(self, other):
        print('__isub__',other)
        return self.match(string)

    def __rsub__(self, other):
        return self.match(other)

    def __call__(self, string):
        return self.match(other)


regexp = Pyjo_Regexp.new

new = Pyjo_Regexp.new
object = Pyjo_Regexp
