"""
Just a short example demonstrating a simple state machine in Python.
This version is doing actual work, downloading the contents of URL's
it gets from a queue. It's also using gevent to get the URL's in an
asynchronous manner.
"""

import gevent
from gevent import monkey

import time
import queue
import requests

monkey.patch_all()


def task(name, work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        print(f"Task {name} getting URL: {url}")
        start_time = time.time()
        elapsed = time.time() - start_time
        requests.get(url)
        print(f"Task {name} got URL: {url}")
        print(f"Task {name} total elapsed time: {elapsed}")


def main():
    """This is main entry point for the program."""
    # Create the queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in the queue.
    for url in [
        "http://google.com",
        "http://yahoo.com",
        "http://linkedin.com",
        "http://shutterfly.com",
        "http://mypublisher.com",
        "http://facebook.com",
    ]:
        work_queue.put(url)

    # Run the tasks.
    start_time = time.time()
    elapsed = time.time() - start_time
    tasks = [
        gevent.spawn(task, "One", work_queue),
        gevent.spawn(task, "Two", work_queue)
    ]
    gevent.joinall(tasks)
    print()
    print(f"Total elapsed time: {elapsed}")


if __name__ == "__main__":
    main()
