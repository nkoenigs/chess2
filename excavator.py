import random
import chess
import chess.pgn
import time

class engine:
    """
    Using recursion
    """
    def __init__(self,tlim):
        self.GLOBAL_HIGH = 100000
        self.GLOBAL_LOW = -self.GLOBAL_HIGH
        self.max_turns = 200
        self.depth = 3
        self.counter = 0 
         
        self.tmargin = .5
        self.tlim = tlim 
        self.turn_tlim = self.tmargin*tlim
        self.last_loop_time = float(tlim*5)

        self.max_depth = 6

        self.piece_values = {
            chess.PAWN : 1,
            chess.KNIGHT : 3,
            chess.BISHOP : 3,
            chess.ROOK : 5,
            chess.QUEEN : 15,
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

    def play(self,board,tlim):
        """
        Play a turn witht the chess engine
        """
        root = chess.pgn.Game()
        root.setup(board.fen())
        self.start_time = time.time()
        self.recursive_tree(root,0,self.depth-1)
        # print("Time for Depth "+str(depth)+"\n\t"+str(end_time-start_time))
        play = self.alphabeta(root,0,self.GLOBAL_LOW,self.GLOBAL_HIGH,root.board().turn) #fix this true
        
        return play.move

    
    def recursive_tree(self,node,depth,depth_lim):
        """
        you spin my head right round right round now
        """
        if (depth<depth_lim):
            for item in node.board().legal_moves:
                node.add_variation(item)
            for var in node.variations:
                self.recursive_tree(var,depth+1,depth_lim)

    
    def time_left(self):
        if (time.time()-self.start_time) > self.turn_tlim:
            return True
        else:
            return False

    def alphabeta(self, node, depth, alpha, beta, max_player):
        pointer = None
        # self.counter+=1
        # print('Count \t'+str(self.counter)+"\t Depth:\t"+str(depth))
        if node.is_end():
            if self.time_left() and depth < 6:
                pboard = node.parent.board()
                nboard = node.board()
                iscap = pboard.is_capture(node.move)
                # pboard.push(node.move)
                if nboard.is_check() or iscap:
                    self.recursive_tree(node,depth+1,depth + 2)
                else:
                    # self.alphabeta
                    return (self.eval_board(node))
                #     pass
            else:
                # print("no time")
                return (self.eval_board(node))
            # print('node end')


        if max_player:
            value = self.GLOBAL_LOW
            for child in node.variations:
                result = self.alphabeta(child, depth + 1, alpha, beta, False)
                if result > value:
                    value = result
                    pointer = child
                alpha = max(alpha, value)
                if alpha >= beta:
                    # print('beta cutoff')
                    break #beta cutoff
            if depth == 0:
                return pointer
            else:
                return value
            # return value, pointer
        else:
            value = self.GLOBAL_HIGH
            for child in node.variations:
                result = self.alphabeta(child, depth + 1, alpha, beta, True)

                if result < value:
                    value = result
                    pointer = child

                beta = min(beta, value)
                if beta <= alpha:
                    # print('alpha cutoff')
                    break #beta cutoff
            if depth == 0:
                return pointer
            else:
                return value

    def eval_board(self,node):
        """
        Evaluate the board position 
            WHITE = MAXIMIZER
            BLACK = minimizer
        """
        ret=0
        board = node.board()
        if(board.is_game_over()):
            res = board.result()
            if res == '1-0':
                ret = self.GLOBAL_HIGH - 1
            elif res == '0-1':
                ret = self.GLOBAL_LOW + 1
            else:
                pass
        else:
            piece_v = 0
            square_v = 0
            map = board.piece_map()
            for square in map:
                piece_v += self.evaluate_piece(map[square])
                square_v += self.evaluate_square(square, map[square])

            ret = piece_v*1000 + square_v
        # node.comment = str(ret)
        ret = ret*random.uniform(.95,1.05)
        return ret

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
