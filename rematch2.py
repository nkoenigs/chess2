import queue as qu
import threading as th
import multiprocessing as mp
import time

import helpers

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
        self.helpers = helpers.methods()
        self.solved_queue = mp.JoinableQueue()
        self.unsolved_queue = mp.JoinableQueue()

        self.all_threads = []
        for i in range(mp.cpu_count - 1)

    def close(self):
        pass

    def play(self, tlim):
        pass
