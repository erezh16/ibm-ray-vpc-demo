import math
import ray
import requests
import numpy as np
import datetime

@ray.remote
def send_query(text):
    ts = datetime.datetime.now()    
    resp = requests.get("http://localhost:8000/?text={}".format(text))
    rtt = (datetime.datetime.now() - ts).total_seconds() * 1000     # Request round-trip time in msec
    return (resp.text, rtt)

def print_results(results):
    print("Results returned:\n")
    sum = 0
    sumsq = 0
    for i in range(n):
        rtt = results[i][1]
        print("[{}] {}\n-----------\nRTT = {}\n-----------\n".format(i, results[i][0], rtt))
        sum += rtt
        sumsq += rtt * rtt
    avg = sum / n
    std = math.sqrt(sumsq / n - avg * avg)
    print("============================\nRTT Average: {} Std.Dev: {}".format(avg, std))

# Let's use Ray to send all queries in parallel
texts = [
    'Once upon a time,',
    'Hi my name is Lewis and I like to',
    'My name is Mary, and my favorite',
    'My name is Clara and I am',
    'My name is Julien and I like to',
    'Today I accidentally',
    'My greatest wish is to',
    'In a galaxy far far away',
    'My best talent is',
    'Call me',
]
n = 100
results = ray.get([send_query.remote(texts[i % len(texts)]) for i in range(n)])
print_results(results)

