import Pyjo.Reactor.Poll

# Dummy reactor
class TestReactor(Pyjo.Reactor.Poll.object):
    pass


def new():
    return TestReactor()
