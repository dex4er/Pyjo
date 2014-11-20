import weakref


class C:
    _ref = None

    def __del__(self):
        print "__del__ " + str(self)

    def ref(self, value=None):
        if value is None:
            return self._ref
        self._ref = weakref.proxy(value)
        return self

def test():
    a = C()
    b = C()

    a.ref(b)
    b.ref(a)

    print "{0}.ref = {1}".format(a, a.ref)
    print "{0}.ref = {1}".format(b, b.ref)


test()
