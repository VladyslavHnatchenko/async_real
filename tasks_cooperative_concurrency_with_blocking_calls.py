"""
Just a short example demonstrating a simple state machine in Python.
However, this one has delays that affect it.
"""

import time
import queue


def task(name, queue):
    while not queue.empty():
        count = queue.get()
        total = 0
        start_time = time.time()
        et = time.time() - start_time
        for x in range(count):
            print(f"Task {name}, running")
            time.sleep(1)
            total += 1
            yield
        print(f"Task {name} total: {total}.")
        print(f"Task {name} total elapsed time: {et}")


def main():
    """This is tne main entry point for the program."""
    # Create the queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in the queue.
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    tasks = [
        task("One", work_queue),
        task("Two", work_queue)
    ]

    # Run the scheduler to run the tasks.
    start_time = time.time()
    et = time.time() - start_time
    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True

    print()
    print(f"Total elapsed time: {et}")


if __name__ == "__main__":
    main()
