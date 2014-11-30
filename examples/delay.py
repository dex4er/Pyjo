from __future__ import print_function

import Pyjo.IOLoop


def step1(delay):
    print("Step 1")
    Pyjo.IOLoop.timer(2, delay.begin())
    Pyjo.IOLoop.timer(1, delay.begin())
    print('Wait 2 seconds for step 2.')


def step2(delay):
    print("Step 2")

    def step2_1(delay2):
        print("Step 2.1")
        end = delay2.begin()
        Pyjo.IOLoop.timer(1, lambda loop: end('','OK'))
        print('Wait 1 second for step 2.2.')

    def step2_2(delay2, *args):
        print("Step 2.2 got {0}".format(args))
        Pyjo.IOLoop.timer(3, delay2.begin())
        print('Wait 3 seconds for step 3.')

    Pyjo.IOLoop.delay().steps(
        step2_1,
        step2_2,
        delay.begin()
    )


def step3(delay):
    print("Step 3")
    print('And done.')


Pyjo.IOLoop.delay().steps(
    step1,
    step2,
    step3
).wait()

print("END")
