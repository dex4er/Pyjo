from Pyjo.Util import nonlocals

class C(object):
    def m(self):
        m = nonlocals()

        m.v = 42

        def s():
            m.v = 666

        s()

        return m.v

o = C()
print(o.m())
