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

rseps = {'(': ')',
         '[': ']',
         '{': '}',
         '<': '>'}


class Pyjo_Regexp(object):

    def __init__(self, action, pattern, replacement='', flags='', lsep='/', rsep='/'):
        self.action = action
        self.pattern = pattern
        self.replacement = replacement
        self.flags = flags
        self.lsep = lsep
        self.rsep = rsep
        self.re_flags = self._re_flags(self.flags)
        self.re = re.compile(self.pattern, self.re_flags)

    @classmethod
    def new(cls, regexp):
        if regexp in CACHE:
            return CACHE[regexp]

        if regexp[0] in 'ms':
            action = regexp[0]
            i = 1
        elif regexp[0] == '/':
            action = 'm'
            i = 0
        else:
            raise ValueError('Bad regexp action: {0}'.format(regexp[0]))

        lsep = regexp[i]
        if lsep in rseps:
            rsep = rseps[lsep]
        else:
            rsep = lsep

        i += 1
        j = i

        while True:
            j2 = regexp.index(rsep, j + 1)
            if j2 == j:
                j += 1
            else:
                j = j2
                if regexp[j - 1] != '\\':
                    break

        pattern = regexp[i:j]

        i = j + 1

        if action == 'm':
            flags = regexp[i:]
            obj = cls(action, pattern, flags=flags, lsep=lsep, rsep=rsep)
            if 'o' not in flags:
                CACHE[regexp] = obj
            return obj

        if lsep in rseps:
            if regexp[i] != lsep:
                raise ValueError('Missing regexp separator: {0}'.format(lsep))
            i += 1

        j = i

        while True:
            j2 = regexp.index(rsep, j + 1)
            if j2 == j:
                j += 1
            else:
                j = j2
                if regexp[j - 1] != '\\':
                    break

        replacement = regexp[i:j]

        i = j + 1

        if action == 's':
            flags = regexp[i:]
            obj = cls(action, pattern, replacement=replacement, flags=flags, lsep=lsep, rsep=rsep)
            if 'o' not in flags:
                CACHE[regexp] = obj
            return obj

        raise ValueError('Bad regexp: {0}'.format(regexp))

    def clone(self):
        new_obj = type(self)(self.action, self.pattern, replacement=self.replacement, flags=self.flags)
        return new_obj

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
            if 'g' in self.flags:
                count = 0
            else:
                count = 1
            return self.re.sub(self.replacement, string, count=count)

    def __eq__(self, other):
        return self.match(other)

    def __rsub__(self, other):
        return self.match(other)

    def __call__(self, string):
        return self.match(string)

    def s(self, replacement):
        new_obj = self.clone()
        new_obj.action = 's'
        new_obj.replacement = replacement
        return new_obj

    def __str__(self):
        string = self.action + self.lsep + self.pattern + self.rsep
        if self.action == 's':
            if self.lsep in rseps:
                string += self.lsep
            string += self.replacement + self.rsep
        string += self.flags
        return string

    def __repr__(self):
        return "regexp('{0}')".format(self)


regexp = Pyjo_Regexp.new
r = regexp

new = Pyjo_Regexp.new
object = Pyjo_Regexp  # @ReservedAssignment
