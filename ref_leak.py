class C:
    ref = None

    def __del__(self):
        print "__del__ " + str(self)


def test():
    a = C()
    b = C()

    a.ref = b
    b.ref = a

    print "{0}.ref = {1}".format(a, a.ref)
    print "{0}.ref = {1}".format(b, b.ref)


test()
