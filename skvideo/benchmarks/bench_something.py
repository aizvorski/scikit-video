# Example benchmark file

import time

def bench_something():
    start = time.clock()
    for k in range(2000):
        k**k
    end = time.clock()

    print("Duration: %r" % (end - start,))

if __name__ == "__main__":
    bench_something()

