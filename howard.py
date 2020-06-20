import random
import chess
import re
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
        self.tlim = tlim 
        self.last_loop_time = float(tlim*5)
        self.reg_parse = re.compile(r"(?:\w|\+|\#|\=|\-){2,6}(?=,|\))")
        self.piece_val = { 'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000, 'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000}
        self.loc_val = {
            'P' : (
                1,  1,  1,  1,  1,  1,  1,  1,
                2,  2,  2,  3,  3,  2,  2,  2,
                2,  2,  3,  4,  4,  3,  2,  2,
                3,  3,  4,  5,  5,  4,  3,  3,
                3,  3,  4,  5,  5,  4,  3,  3,
                2,  2,  2,  3,  3,  2,  2,  2,
                1,  1,  1,  1,  1,  1,  1,  1,
            ),
            'N' : (
                 1,	1,	1,	1,	1,	1,	1,	1,
                2,	2,	2,	3,	3,	2,	2,	2,
                2,	2,	3,	4,	4,	3,	2,	2,
                3,	3,	4,	5,	5,	4,	3,	3,
                3,	3,	4,	5,	5,	4,	3,	3,
                2,	2,	3,	4,	4,	3,	2,	2,
                2,	2,	2,	3,	3,	2,	2,	2,
                1,	1,	1,	1,	1,	1,	1,	1, 
            ), 
           'B' : (
                1,	1,	1,	1,	1,	1,	1,	1,
                2,	2,	2,	3,	3,	2,	2,	2,
                2,	2,	3,	4,	4,	3,	2,	2,
                3,	3,	4,	5,	5,	4,	3,	3,
                3,	3,	4,	5,	5,	4,	3,	3,
                2,	2,	3,	4,	4,	3,	2,	2,
                2,	2,	2,	3,	3,	2,	2,	2,
                1,	1,	1,	1,	1,	1,	1,	1, 
            ),
            'R' : (
                1,	1,	1,	1,	1,	1,	1,	1,
                2,	2,	2,	3,	3,	2,	2,	2,
                2,	2,	3,	4,	4,	3,	2,	2,
                3,	3,	4,	5,	5,	4,	3,	3,
                3,	3,	4,	5,	5,	4,	3,	3,
                2,	2,	3,	4,	4,	3,	2,	2,
                2,	2,	2,	3,	3,	2,	2,	2,
                1,	1,	1,	1,	1,	1,	1,	1, 
            ),
            'Q' : (
                1,	1,	1,	1,	1,	1,	1,	1,
                2,	2,	2,	3,	3,	2,	2,	2,
                2,	2,	3,	4,	4,	3,	2,	2,
                3,	3,	4,	5,	5,	4,	3,	3,
                3,	3,	4,	5,	5,	4,	3,	3,
                2,	2,	3,	4,	4,	3,	2,	2,
                2,	2,	2,	3,	3,	2,	2,	2,
                1,	1,	1,	1,	1,	1,	1,	1, 
            ),
            'K' : (
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
            ),
        }
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



    def legal_move_list(self,board):
        """
        Get a list of legal moves in san notation
        """
        leg_move = board.legal_moves
        leg_move_list = re.findall(self.reg_parse,str(leg_move))
        return leg_move_list

    def board_value(self,board,player_col):
        """
        Evaluate the board position to good bad number

        player_col:
            WHITE = 1
            BLACK = -1
        """

        value = 0
        pmap = board.piece_map()
        for key in pmap:
            peice = pmap[key]
            value += self.piece_val[peice.symbol()]*player_col

            if peice.color and player_col == 1:
                value += self.loc_val[peice.symbol()][key]
            elif not(peice.color) and player_col == -1:
                value += self.loc_val[peice.symbol().capitalize()][63 - key]
        

        return value
        # return 2

    def play(self,board,tlim):
        """
        Play a turn witht the chess engine
        """
        if not hasattr(self,'color'):
            if board.turn == chess.WHITE:
                # print('WHITE\n\n')
                self.color = 1 #
                self.agent = True
            else:
                # print("BLACK\n\n")
                self.color = -1
                self.agent = False

        if board.fullmove_number < self.max_turns:
            root = chess.pgn.Game()
            root.setup(board.fen())
            start_time = time.time()
            self.recursive_tree(root,0,self.depth)
            # print("Time for Depth "+str(depth)+"\n\t"+str(end_time-start_time))
            play = self.alphabeta(root,0,self.GLOBAL_LOW,self.GLOBAL_HIGH,root.board().turn) #fix this true
            end_time = time.time()
            self.last_loop_time = end_time - start_time
            
            print("self depth:\t"+str(self.depth)+'\tcounter'+str(self.counter))
            print('tdiff\t'+str(self.last_loop_time*5)+"\ttlim\t"+str(self.tlim))

            if (self.last_loop_time*10<self.tlim):
                if self.counter > 10:
                    self.depth += 1
                    print("\t!!!\tincreasing depth\t!!!")
            elif (self.last_loop_time>self.tlim):
                if self.depth>3:
                    self.depth -= 1
                    print("\t!!!\tdecreaseing depth\t!!!")

            # print('Move Val:\t'+str(val))
            self.counter += 1
            return play.move
        else:
            return chess.Move.null()
    
    def recursive_tree(self,node,depth,depth_lim):
        """
        you spin my head right round right round now
        """
        if (depth<depth_lim):
            for item in node.board().legal_moves:
                node.add_variation(item)
            for var in node.variations:
                self.recursive_tree(var,depth+1,depth_lim)
                # print(depth)
                
    def alphabeta(self, node, depth, alpha, beta, max_player):
        pointer = None
        # self.counter+=1
        # print('Count \t'+str(self.counter)+"\t Depth:\t"+str(depth))
        if node.is_end():
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

                beta = min(alpha, value)
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
        # ret = ret*random.uniform(.95,1.05)
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
