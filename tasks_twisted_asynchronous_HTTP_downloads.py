"""
Just a short example demonstrating a simple state machine in Python.
This version is doing actual work, downloading the contents of URL's
it gets from a work_queue. This version uses the Twisted framework to
provide the concurrency.
"""

import queue
import time

from twisted.internet import defer, reactor, task
from twisted.web.client import getPage


@defer.inlineCallbacks
def my_task(name, work_queue):
    try:
        while not work_queue.empty():
            url = work_queue.get()
            print(f"Task {name} getting URL: {url}")
            start_time = time.time()
            elapsed_time = time.time() - start_time
            yield getPage(url)
            print(f"Task {name} got URL: {url}")
            print(f"Task {name} total elapsed time: {elapsed_time}")
    except Exception as e:
        print(str(e))


def main():
    """This is main entry point for the program."""
    # Create the work_queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in the work_queue
    for url in [
        b"http://google.com",
        b"http://yahoo.com",
        b"http://linkedin.com",
        b"http://shutterfly.com",
        b"http://mypublisher.com",
        b"http://facebook.com"
    ]:
        work_queue.put(url)

    # Run the tasks.
    start_time = time.time()
    elapsed_time = time.time() - start_time
    defer.DeferredList([
        task.deferLater(reactor, 0, my_task, "One", work_queue),
        task.deferLater(reactor, 0, my_task, "Two", work_queue)
    ]).addCallback(lambda _: reactor.stop())

    # Run the event loop.
    reactor.run()

    print()
    print(f"Total elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
