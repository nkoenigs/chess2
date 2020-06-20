import multiprocessing as mp
import time
import chess

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
        self.solved_queue = mp.Queue()
        self.unsolved_queue = mp.JoinableQueue()
        self.active_requests = 0

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
        if bool(board.legal_moves) == False:
            return chess.Move.null()
        move_list = board.legal_moves

        for move in move_list:
            self.unsolved_queue.put([move, 0])
            self.active_requests += 1
        self.unsolved_queue.join()

        # get the workers results for each board
        move_list = []
        while self.active_requests > 0:
            if not self.solved_queue.empty():
                rated_move = self.solved_queue.get()
                move_list.append(rated_move)
                self.active_requests -= 1

        # play the highest rated move
        highest_rated = ["", 0]
        for move in move_list:
            if move[1] > highest_rated[1]:
                highest_rated = move

        return highest_rated[0]
        


