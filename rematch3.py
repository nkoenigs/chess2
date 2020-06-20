import time
import chess
import chess.pgn
import random

'uh oh here here i go again...'
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
        self.start_time = 0
        self.tlim = tlim

    def play(self, board, tlim):
        time0 = time.time()
        self.start_time = time0
        self.key_counter = 0
        self.keys_left = 0
        self.root = chess.pgn.Game()
        self.root.setup(board.fen())
        self.help.add_noise()

        for _ in range(self.layers):
            self.grow_layer(self.root)

        # time1 = time.time()
        # print("build time = " + str(time1 - time0))

        play = self.minmax(self.root, GLOBAL_MIN, GLOBAL_MAX, self.root.board().turn, 0)
        move = play.move

        # time2 = time.time()
        # print("huristic time = " + str(time2 - time1))

        return move
        
    def compute_value(self, board):
        """
        finds the value of the current board
        """
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
                ret += self.help.evaluate_pawn_advantage(square, map[square])
        return ret
    
    def grow_layer(self, node):
        """
        grows a layer at the end of all branches from the given node
        """
        if node.is_end():
            for move in node.board().legal_moves:
                node.add_variation(move)
        elif not node.board().is_game_over():
            for child in node.variations:
                self.grow_layer(child)
        
    def minmax(self, node, alpha, beta, im_max, depth):
        """
        implements alpha beta parsing of a huristics tree
        if time is avaible will extend the tree in intresting situations
        """
        if node.is_end():
            board = node.parent.board()
            is_cap = board.is_capture(node.move)
            board.push(node.move)
            if board.is_game_over():
                return self.help.test_checkmate(board)
            elif (board.is_check() or is_cap) and (time.time() - self.start_time < 0.5 * self.tlim) and (depth < 8):
                self.grow_layer(node)
            else:
                return self.compute_value(board)
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
                print('odds are ' + str(value))
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
    """
    helper to evaluate the board with
    """
    def __init__(self):
        self.piece_values = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 9,
            chess.KING : 1
        }
        self.transform_tuple = (
            0, 8, 7, 6, 5, 4, 3, 2,1
        )
        self.square_values_master = [
            1, 2, 2, 2, 2, 2, 2, 1,
             1, 2, 1, 1, 1, 1, 2, 1, 
             1, 5, 8, 6, 6, 8, 5, 1, 
             1, 3, 6, 9, 9, 6, 3, 1, 
             1, 3, 6, 9, 9, 6, 3, 1, 
             1, 5, 8, 6, 6, 8, 5, 1,
             1, 2, 1, 1, 1, 1, 2, 1,
             1, 2, 2, 2, 2, 2, 2, 1
        ]
        self.square_values = self.square_values_master.copy()

    def add_noise(self):
        self.square_values = self.square_values_master.copy()
        for sq in range(64):
            rand = random.randrange(-100,100)/80
            self.square_values[sq] += rand

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

    def evaluate_pawn_advantage(self, square, piece):
        if not piece == chess.PAWN:
            return 0
        rank = chess.square_rank(square)
        if not piece.color:
            rank = self.transform_tuple[rank]
        return rank

    def test_checkmate(self, board):
        try:
            res = board.result()
            if res == '1-0':
                return GLOBAL_MAX - 1
            if res == '0-1':
                return GLOBAL_MIN + 1
            return 0
        except:
            return 0