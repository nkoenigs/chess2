import multiprocessing as mp
import time
import chess
import chess.pgn
import random

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
        self.active_nodes = []

    def request(self):
        """
        create a pool of workers for main to start
        """
        pool = []
        for _ in range(mp.cpu_count() - 1):
            new_thread = mp.Process(target= run, args= (self.unsolved_queue, self.solved_queue, ))
            new_thread.daemon = True
            pool.append(new_thread)
        return pool

    def close(self):
        pass

    def play(self, board, tlim):
        # some setup
        start_time = time.time()
        leaves = self.create_root(board)

        leaves_copy = leaves.copy()
        for leaf in leaves_copy:
            self.grow_branch(leaves, leaf)

        for leaf in leaves:
            print(leaf.metrics.value)


        # # get all legal moves
        # if bool(board.legal_moves) == False:
        #     return chess.Move.null()
        # move_list = board.legal_moves

        # for move in move_list:
        #     self.unsolved_queue.put([move, 0])
        #     self.active_requests += 1
        # self.unsolved_queue.join()

        # # get the workers results for each board
        # move_list = []
        # while self.active_requests > 0:
        #     if not self.solved_queue.empty():
        #         rated_move = self.solved_queue.get()
        #         move_list.append(rated_move)
        #         self.active_requests -= 1

        # # play the highest rated move
        # highest_rated = ["", 0]
        # for move in move_list:
        #     if move[1] > highest_rated[1]:
        #         highest_rated = move

        # return highest_rated[0]

    def create_root(self, board):
        """
        makes a root for the tree
        then grows the first layer
        returns the leaves
        """
        root = chess.pgn.Game.from_board(board)
        leaves = []
        for move in root.board().legal_moves:
            new_node = root.add_variation(move)
            new_node.metrics = metrics(move)
            self.unsolved_queue.put(new_node)
            self.active_requests += 1
        self.unsolved_queue.join()

        while self.active_requests > 0:
            if not self.solved_queue.empty():
                leaves.append(self.solved_queue.get())
                self.active_requests -= 1

        return leaves

    def grow_branch(self, leaves, parent):
        """
        creates child nodes for all avalible moves from a given parent gameNode
        also modifies the leaves
        returns a list of all new leaves
        """
        leaves.remove(parent)

        for move in parent.board().legal_moves:
            new_node = parent.add_variation(move)
            new_node.metrics = parent.metrics.childs_metrics()
            self.unsolved_queue.put(new_node)
            self.active_requests += 1
        self.unsolved_queue.join()

        while self.active_requests > 0:
            if not self.solved_queue.empty():
                leaves.append(self.solved_queue.get())
                self.active_requests -= 1        

        return new_leaves

def run(unsolved_queue, solved_queue):
    """
    run this as a process in the background
    use queues to pass in ideas to evaluate
    """
    while True:
        if not unsolved_queue.empty():
            node = unsolved_queue.get()

            node.metrics.value = random.randrange(100)

            solved_queue.put(node)
            unsolved_queue.task_done()


class metrics:
    """
    An idea is complex object desgined to help workers evaluate moves
    """
    def __init__(self, move):
        self.depth = 1
        self.root_move = move
        self.value = None
        self.interest = None

    def childs_metrics(self):
        """
        returns updated metrics for my child
        """
        childs = metrics(None)
        childs.depth = self.depth + 1
        childs.root_move = self.root_move
        return childs

class pickleable_data:
    """
    a class to enable passing relivant data through a queue
    """
    def __init__(self, node, index)
    self.metrics = node.metrics
    self.index = index
    self.after = node.board()
