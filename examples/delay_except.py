import Pyjo.IOLoop

# Handle exceptions in all steps
delay = Pyjo.IOLoop.delay()


@delay.step
def step1(delay):
    raise Exception('Intentional error')


@delay.step
def step2(delay):
    print('Never actually reached.')


@delay.catch
def error(delay, err):
    print("Something went wrong: {0}".format(err))


delay.wait()
