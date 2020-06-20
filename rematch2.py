import queue as qu
import threading as th
import multiprocessing as mp
import time

import helpers
import worker

'uh oh here here i go again...'

class engine:
    """
    R.edesigned
    E.ntrylevel
    M.ultithreaded
    A.pproach
    T.o A
    C.hess
    H.andling
    ENGINE
    2 
    """
    def __init__(self, tlim):
        # create helper object for parsing nonsence
        self.helpers = helpers.methods()

        # create queues for interacting with forign threads
        self.solved_queue = mp.JoinableQueue()
        self.unsolved_queue = mp.JoinableQueue()

        # create and start a pool of workers
        self.my_pool = []
        for _ in range(mp.cpu_count() - 1):
            new_thread = mp.Process(target= worker.run, args= (self.unsolved_queue, self.solved_queue, ))
            self.my_pool.append(new_thread)
        for thread in self.my_pool:
            thread.start()

    def close(self):
        pass

    def play(self, board, tlim):
        pass
