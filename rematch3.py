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
    3
    """
    def __init__(self, tlim):
        self.root = None
        self.layers = 3
        self.help = helper()

    def request(self):
        return []

    def close(self):
        pass

    def play(self, board, tlim):
        # some setup
        time0 = time.time()
        self.key_counter = 0
        self.keys_left = 0
        self.root = chess.pgn.Game()
        self.root.setup(board.fen())

        for _ in range(self.layers):
            self.grow_layer(self.root)

        time1 = time.time()
        print("build time = " + str(time1 - time0))

        play = self.minmax(self.root, GLOBAL_MIN, GLOBAL_MAX, self.root.board().turn, 0)
        move = play.move

        time2 = time.time()
        print("huristic time = " + str(time2 - time1))

        return move
        
    def compute_value(self, node):
        board = node.board()
        ret = 0
        if(board.is_game_over()):
            res = board.result()
            if res == '1-0':
                ret = GLOBAL_MAX - 1
            elif res == '0-1':
                ret = GLOBAL_MIN + 1
            else:
                pass
        else:
            map = board.piece_map()
            for square in map:
                ret += self.help.evaluate_piece(map[square]) * 1000
                ret += self.help.evaluate_square(square, map[square]) * 10
            # ret += self.help.evaluate_attacks(board)
        return ret
    
    def grow_layer(self, node):
        if node.is_end():
            for move in node.board().legal_moves:
                node.add_variation(move)
        elif not node.board().is_game_over():
            for child in node.variations:
                self.grow_layer(child)
        
    def minmax(self, node, alpha, beta, im_max, depth):
        if node.is_end():
            return self.compute_value(node)
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
                print('odds are' + str(value))
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
                print('odds are ' + str(value))
                return pointer
            else:
                return value

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
        self.square_values = (
            1, 2, 2, 2, 2, 2, 2, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 
             1, 5, 8, 6, 6, 8, 5, 1, 
             1, 1, 6, 9, 9, 6, 1, 1, 
             1, 1, 6, 9, 9, 6, 1, 1, 
             1, 5, 8, 6, 6, 8, 5, 1,
             1, 1, 1, 1, 1, 1, 1, 1,
             1, 2, 2, 2, 2, 2, 2, 1
            )

    def evaluate_square(self, square, piece):
        value = self.square_values[square]
        if not piece.color:
            value *= -1
        return value

    def evaluate_piece(self, piece):
        value = self.piece_values[piece.piece_type]
        if not piece.color:
            value *= -1
        return value

    def evaluate_attacks(self, board):
        value = 0
        for square in range(64):
            value += len(board.attackers(True, square))
            value -= len(board.attackers(False, square))
        return value