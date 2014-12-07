import Pyjo.IOLoop


@Pyjo.IOLoop.recurring(0)
def print_cb(loop):
    print("A")


@Pyjo.IOLoop.timer(1)
def stop_cb(loop):
    loop.stop()


Pyjo.IOLoop.start()
