import Pyjo.IOLoop


loop = Pyjo.IOLoop.singleton()


@loop.recurring(0)
def print_cb(loop):
    print("A")


@loop.timer(1)
def stop_cb(loop):
    loop.stop()


loop.start()
