import weakref


class C:
    ref = None

    def __del__(self):
        print "__del__ " + str(self)


def test():
    a = C()
    b = C()

    a.ref = weakref.proxy(b)
    b.ref = weakref.proxy(a)

    print "{0}.ref = {1}".format(a, a.ref)
    print "{0}.ref = {1}".format(b, b.ref)


test()
