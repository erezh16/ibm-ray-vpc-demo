import math
import ray
import requests
import numpy as np
import datetime
import click

@ray.remote
def send_query(text):
    ts = datetime.datetime.now()    
    resp = requests.get("http://localhost:8000/?text={}".format(text))
    rtt = (datetime.datetime.now() - ts).total_seconds() * 1000     # Request round-trip time in msec
    return (resp.text, rtt)

def print_results(results,request_num):
    print("Results returned:\n")
    sum = 0
    sumsq = 0
    for i in range(request_num):
        rtt = results[i][1]
        print("[{}] {}\n-----------\nRTT = {}\n-----------\n".format(i, results[i][0], rtt))
        sum += rtt
        sumsq += rtt * rtt
    avg = sum / request_num
    std = math.sqrt(sumsq / request_num - avg * avg)
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

@click.command()
@click.option('--requests', '-r', show_default=True, default=10, help=f'number of concurrent requests')
def builder(requests):
    results = ray.get([send_query.remote(texts[i % len(texts)]) for i in range(requests)])
    print_results(results,requests)

if __name__ == '__main__':
    builder()