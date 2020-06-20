import multiprocessing as mp
import time
import chess
import chess.pgn
import random

'uh oh here here i go again...'
key_counter = 0

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
        self.leaves = []
        self.root = None
        self.node_keys = {}
        self.alpha = None
        self.beta = None

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
        self.create_root(board)

        leaves_copy = self.leaves.copy()
        for leaf in leaves_copy:
            self.grow_branch(leaf)

        # for leaf in self.leaves:
        #     print("val: " + str(leaf.metrics.value))

    def send_node_to_workers(self, node):
        """
        this function sends data to the queues to evaluate a board
        """
        data = pickleable_data(node)
        self.node_keys[data.key] = node
        self.unsolved_queue.put(data)

    def collect_work(self):
        """
        puts unpickled data into its node
        """
        while len(self.node_keys) > 0:
            if not self.solved_queue.empty():
                data = self.solved_queue.get()
                node = self.node_keys.pop(data.key)
                node.metrics.value = data.value
                node.metrics.interest = data.interest
                self.leaves.append(node)

    def create_root(self, board):
        """
        makes a root for the tree
        then grows the first layer
        """
        self.root = chess.pgn.Game()
        self.root.setup(board.fen())

        for move in self.root.board().legal_moves:
            new_node = self.root.add_variation(move)
            new_node.metrics = metrics(move)
            self.send_node_to_workers(new_node)

        self.unsolved_queue.join()
        self.collect_work()

    def grow_branch(self, parent):
        """
        creates child nodes for all avalible moves from a given parent gameNode
        also modifies the leaves
        """
        self.leaves.remove(parent)
        for move in parent.board().legal_moves:
            new_node = parent.add_variation(move)
            new_node.metrics = parent.metrics.childs_metrics()
            self.send_node_to_workers(new_node)

        self.unsolved_queue.join()
        self.collect_work()

    def minmax(self):
        """
        alpha beta mixmaxing
        returns the best move
        """
        self.alpha = -10000000
        self.beta = 10000000
        self.recure(root, self.root.board().turn)

    def recur(self, loc, is_max):
        """
        im sorry father i have sinned, i had no other option
        forgive me
        """


def run(unsolved_queue, solved_queue):
    """
    run this as a process in the background
    use queues to pass in ideas to evaluate
    """
    while True:
        if not unsolved_queue.empty():
            pkobj = unsolved_queue.get()

            rand = random.randrange(100) - 50
            ret = unpickleable_data(rand, rand, pkobj.key)

            solved_queue.put(ret)
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
    def __init__(self, node):
        global key_counter
        self.after_fen =  node.board().fen()
        self.before_fen = node.parent.board().fen()
        self.move = node.move 
        self.key = key_counter
        key_counter += 1

class unpickleable_data:
    def __init__(self, value, interest, key):
        self.key = key
        self.value = value 
        self.interest = interest