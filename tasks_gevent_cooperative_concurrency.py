"""
Just a short example demonstrating a simple state machine in Python.
However, this one has delays that affect it.
"""
import time
import queue
import gevent
from gevent import monkey

monkey.patch_all()


def task(name, work_queue):
    while not work_queue.empty():
        count = work_queue.get()
        total = 0
        start_time = time.time()
        elapsed = time.time() - start_time
        for x in range(count):
            print(f"Task {name} running.")
            time.sleep(1)
            total += 1
        print(f"Task {name} total: {total}")
        print(f"Task {name} total elapsed time: {elapsed}")


def main():
    """This is the main entry point for the program."""
    # create the queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in the queue.
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

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
