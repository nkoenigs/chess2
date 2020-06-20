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
        self.solved_queue = mp.Queue()
        self.unsolved_queue = mp.JoinableQueue()

    def request(self):
        """
        create a pool of workers for main to start
        """
        pool = []
        for _ in range(mp.cpu_count() - 1):
            new_thread = mp.Process(target= worker.run, args= (self.unsolved_queue, self.solved_queue, ))
            new_thread.daemon = True
            pool.append(new_thread)
        return pool

    def close(self):
        pass

    def play(self, board, tlim):
        # get all legal moves
        move_list = []
        board_list = self.helpers.getLegalMoveList(board)
        for board in board_list:
            move_list.append([board , 0])

        # send moves for all boards to workers
        for move in move_list:
            self.unsolved_queue.put(move)
        self.unsolved_queue.join()

        # get the workers results for each board
        final_move_list = []
        while not self.solved_queue.empty():
            rated_move = self.solved_queue.get()
            final_move_list.append(rated_move)

        # play the highest rated move
        highest_rated = ["", 0]
        for move in final_move_list:
            if move[1] > highest_rated[1]:
                highest_rated = move

        return highest_rated[0]
        


