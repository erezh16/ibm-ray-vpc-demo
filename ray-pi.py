import ray
import random
import time
import math
from fractions import Fraction
from statistics import mean

# Let's start Ray
ray.init()

@ray.remote
def pi4_sample(sample_count):
    """pi4_sample runs sample_count experiments, and returns the 
    fraction of time it was inside the circle. 
    """
    in_count = 0
    for i in range(sample_count):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            in_count += 1
    return Fraction(in_count, sample_count)


BATCH_SIZE = 1000 * 1000
BATCH_COUNT = 1000
TOTAL_COUNT = BATCH_SIZE * BATCH_COUNT
start = time.time()
pi4 = mean(ray.get([pi4_sample.remote(sample_count = BATCH_SIZE) for i in range(BATCH_COUNT)]))
end = time.time()
dur = end - start
print(f'Running {TOTAL_COUNT} tests took {dur} seconds')
pi = float(pi4 * 4)
err = abs(pi - math.pi) / pi
print(f'Computed PI = {pi} Error = {err}')