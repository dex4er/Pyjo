import Pyjo.IOLoop


delay = Pyjo.IOLoop.delay()


@delay.step
def step1(delay):
    print("Step 1")
    Pyjo.IOLoop.timer(delay.begin(), 2)
    Pyjo.IOLoop.timer(delay.begin(), 1)
    print('Wait 2 seconds for step 2.')


@delay.step
def step2(delay):
    print("Step 2")

    delay2 = Pyjo.IOLoop.delay()

    @delay2.step
    def step2_1(delay2):
        print("Step 2.1")
        end = delay2.begin()
        Pyjo.IOLoop.timer(lambda loop: end('', 'OK'), 1)
        print('Wait 1 second for step 2.2.')

    @delay2.step
    def step2_2(delay2, *args):
        print("Step 2.2 got {0}".format(args))
        Pyjo.IOLoop.timer(delay2.begin(), 3)
        print('Wait 3 seconds for step 3.')

    delay2.step(delay.begin()).wait()


@delay.step
def step3(delay):
    print("Step 3")
    print('And done.')


delay.wait()

print("END")
