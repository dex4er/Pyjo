import Pyjo.IOLoop


def a(loop):
    print("A")


def fail(loop):
    print("OOPS!")
    # loop.reactor.emit('error', 'BOOM!');
    loop.stop()


Pyjo.IOLoop.recurring(0, a)
Pyjo.IOLoop.timer(1, fail)

Pyjo.IOLoop.start()
