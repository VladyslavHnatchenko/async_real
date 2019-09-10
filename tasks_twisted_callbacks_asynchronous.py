"""
Just a short example demonstrating a simple state machine in Python.
This version is doing actual work, downloading the contents of URL's
it gets from a queue. This version uses the Twisted framework to provide
the concurrency.
"""

import time
import queue

from twisted.internet import defer, reactor, task
from twisted.web.client import getPage


def success_callback(results, name, url, elapsed_time):
    print(f"Task {name} got URL: {url}")
    print(f"Task {name}, total elapsed time: {elapsed_time}")


def my_task(name, queue):
    if not queue.empty():
        while not queue.empty():
            url = queue.get()
            print(f"Task {name} getting URL: {url}")
            start_time = time.time()
            elapsed_time = time.time() - start_time
            d = getPage(url)
            d.addCallback(success_callback, name, url, elapsed_time)
            yield d


def main():
    """This is main entry point for the program."""
    # Create the queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in th queue.
    for url in [
        b"http://google.com",
        b"http://yahoo.com",
        b"http://linkedin.com",
        b"http://sutterfly.com",
        b"http://mypublisher.com",
        b"http://facebook.com"
    ]:
        work_queue.put(url)

    # Run the tasks:
    start_time = time.time()
    elapsed = time.time() - start_time

    # Create cooperator.
    coop = task.Cooperator()

    defer.DeferredList([
        coop.coiterate(my_task("One", work_queue)),
        coop.coiterate(my_task("Two", work_queue)),
    ]).addCallback(lambda _: reactor.stop())

    # Run the event loop.
    reactor.run()

    print()
    print(f"Total elapsed time: {elapsed}")


if __name__ == "__main__":
    main()
