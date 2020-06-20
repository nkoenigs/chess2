import multiprocessing as mp
import time
import chess
import chess.pgn
import random

'uh oh here here i go again...'
key_counter = 0
GLOBAL_MIN = -1000000
GLOBAL_MAX = 1000000

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
        self.root = None
        self.node_keys = {}

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
        time0 = time.time()
        self.root = chess.pgn.Game()
        self.root.setup(board.fen())

        self.grow_layer(self.root)
        self.grow_layer(self.root)
        self.grow_layer(self.root)
        self.grow_layer(self.root)

        time1 = time.time()
        print("build time = " + str(time1 - time0))

        self.find_heuristics(self.root)

        time2 = time.time()
        print("huristic time = " + str(time2 - time1))

        play = self.minmax(self.root, GLOBAL_MIN, GLOBAL_MAX, self.root.board().turn, 0)
        move = play.move

        time3 = time.time()
        print("minmax time = " + str(time3 - time2))

        return move

        # for leaf in self.leaves:
        #     print("val: " + str(leaf.metrics.value))

    def find_heuristics(self, node):
        if len(node.variations) == 0:
            node.comment = str(compute_value(node))
        else:
            for child in node.variations:
                self.find_heuristics(child)
        

    def collect_work(self):
        """
        puts unpickled data into its node
        """
        while len(self.node_keys) > 0:
            if not self.solved_queue.empty():
                data = self.solved_queue.get()
                node = self.node_keys.pop(data.key)
                node.comment = str(data.value)

    def grow_layer(self, node):
        if len(node.variations) == 0:
            for move in node.board().legal_moves:
                node.add_variation(move)
        else:
            for child in node.variations:
                self.grow_layer(child)
                
        # def grow_branch(self, parent):
        #     """
        #     creates child nodes for all avalible moves from a given parent gameNode
        #     also modifies the leaves
        #     """
        #     for move in parent.board().legal_moves:
        #         parent.add_variation(move)
        
    def minmax(self, node, alpha, beta, im_max, depth):
        if len(node.variations) == 0:
            return int(node.comment)
        pointer = None
        if im_max:
            value = GLOBAL_MIN
            for child in node.variations:
                res = self.minmax(child, alpha, beta, False, depth + 1)
                if res > value:
                    value = res
                    pointer = child
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            if depth == 0:
                return pointer
            else:
                return value
        else:
            value = GLOBAL_MAX
            for child in node.variations:
                res  = self.minmax(child, alpha, beta, True, depth + 1)
                if res < value:
                    value = res
                    pointer = child
                beta = min(beta, value)
                if beta <= alpha:
                    break
            if depth == 0:
                return pointer
            else:
                return value

def compute_value(node):
    return random.randrange(100) - 50

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