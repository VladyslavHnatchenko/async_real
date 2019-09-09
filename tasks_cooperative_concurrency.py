"""
Just a short example demonstrating a simple state machine in Python.
"""

import queue


def task(name, queue):
    while not queue.empty():
        count = queue.get()
        total = 0
        for x in range(count):
            print(f"Task {name} running.")
            total += 1
            yield
        print(f"Task {name} total: {total}.")


def main():
    """This is main entry point for the program."""
    # Create the queue of "work".
    work_queue = queue.Queue()

    # Put some "work" in the queue.
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Create some tasks.
    tasks = [
        task("One", work_queue),
        task("Two", work_queue)
    ]

    # Run the tasks.
    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True


if __name__ == "__main__":
    main()
