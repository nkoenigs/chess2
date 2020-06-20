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
        self.unsolved_queue = mp.Queue()
        self.root = None
        self.key_counter = 0
        self.keys_left = 0
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
        self.key_counter = 0
        self.keys_left = 0
        self.root = chess.pgn.Game()
        self.root.setup(board.fen())

        self.grow_layer(self.root)
        self.grow_layer(self.root)
        self.grow_layer(self.root)

        time1 = time.time()
        print("build time = " + str(time1 - time0))

        self.find_heuristics(self.root)
        self.assign_heuristics()

        time2 = time.time()
        print("huristic time = " + str(time2 - time1))

        play = self.minmax(self.root, GLOBAL_MIN, GLOBAL_MAX, self.root.board().turn, 0)
        move = play.move

        time3 = time.time()
        print("minmax time = " + str(time3 - time2))
        print("number of huristics computed = " + str(self.key_counter))

        return move

        # for leaf in self.leaves:
        #     print("val: " + str(leaf.metrics.value))

    def find_heuristics(self, node):
        if node.is_end():
            self.compute_value(node)
        else:
            for child in node.variations:
                self.find_heuristics(child)
        
    def compute_value(self, node):
        fen = node.board().fen()
        key = self.key_counter
        self.key_counter += 1
        self.keys_left += 1
        self.node_keys[key] = node
        pickle = (fen, key)
        self.unsolved_queue.put(pickle)
    
    def assign_heuristics(self):
        while self.keys_left > 0:
            if not self.solved_queue.empty():
                hold = self.solved_queue.get()
                self.node_keys[hold[1]].comment = str(hold[0])
    
                self.keys_left -= 1
    
    def grow_layer(self, node):
        if node.is_end():
            for move in node.board().legal_moves:
                node.add_variation(move)
        else:
            for child in node.variations:
                self.grow_layer(child)
        
    def minmax(self, node, alpha, beta, im_max, depth):
        if node.is_end():
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

def run(unsolved_queue, solved_queue):
    """
    run this as a process in the background
    use queues to pass in ideas to evaluate
    """
    board = chess.Board()
    help = helper()
    while True:
        if not unsolved_queue.empty():
            pickle = unsolved_queue.get()
            fen = pickle[0]
            ret = 0
            board.set_fen(fen)

            if(board.is_game_over()):
                res = board.result()
                if res == '1-0':
                    ret = GLOBAL_MAX - 1
                elif res == '0-1':
                    ret = GLOBAL_MIN + 1
                else:
                    pass
            else:
                net_piece_value = 0
                map = board.piece_map()
                for square in map:
                    net_piece_value += help.evaluate_piece(map[square])

                ret = net_piece_value

            out = (ret, pickle[1])
            solved_queue.put(out)

class helper:
    def __init__(self):
        self.piece_values = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 9,
            chess.KING : 1
        }

    def evaluate_piece(self, piece):
        value = self.piece_values[piece.piece_type]
        if not piece.color:
            value *= -1
        return value