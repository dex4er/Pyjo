import Pyjo.IOLoop


def print_cb(loop):
    print("A")


def stop_cb(loop):
    loop.stop()


Pyjo.IOLoop.recurring(0, print_cb)
Pyjo.IOLoop.timer(1, stop_cb)

Pyjo.IOLoop.start()
