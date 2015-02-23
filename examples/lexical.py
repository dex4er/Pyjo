class C(object):
    def m(self):
        v = 42

        def s():
            v = 666

        s()

        return v

o = C()
print(o.m())
