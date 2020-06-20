import multiprocessing as mp
import time
import random

import helpers


def run(unsolved_queue, solved_queue):
    while True:
        if not unsolved_queue.empty():
            move = unsolved_queue.get()
            move[1] = random.randrange(1000)
            solved_queue.put(move)
            unsolved_queue.task_done()

