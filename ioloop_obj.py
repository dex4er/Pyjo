import Pyjo.IOLoop


def print_cb(loop):
    print("A")


def stop_cb(loop):
    loop.stop()


loop = Pyjo.IOLoop.singleton()

loop.recurring(0, print_cb)
loop.timer(1, stop_cb)

loop.start()
