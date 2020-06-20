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
        self.max_turns = 75
        self.turn = 0       
        self.tlim = tlim 
        self.reg_parse = re.compile(r"(?:\w|\+|\#|\=|\-){2,6}(?=,|\))")
        self.piece_val = { 'P': 10, 'N': 25, 'B': 30, 'R': 50, 'Q': 100, 'K': 1000, 'p': -10, 'n': -25, 'b': -30, 'r': -50, 'q': -100, 'k': -1000}
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
        time0 = time.time()
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
            # start_time = time.time()
            depth = 3
            self.recursive_tree(root,0,depth)
            time1 = time.time()
            # end_time = time.time()
            # print("Time for Depth "+str(depth)+"\n\t"+str(end_time-start_time))
            alpha = 1000
            beta = -alpha
            val, play = self.alphabeta(root,0,alpha,beta,self.agent) #fix this true
            time2 = time.time()

            print("A build time = " + str(time1 - time0))
            print("A huristic time = " + str(time2 - time1))

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
        if node.is_end():
            return (self.eval_board(node), pointer)
        if max_player:
            value = -10000000
            for child in node.variations:
                result, _ = self.alphabeta(child, depth + 1, alpha, beta, False)

                if result > value:
                    value = result
                    pointer = child

                alpha = max(alpha, value)
                if alpha >= beta:
                    break #beta cutoff
            return value, pointer
        else:
            value = 10000000
            for child in node.variations:
                result, _ = self.alphabeta(child, depth + 1, alpha, beta, True)

                if result < value:
                    value = result
                    pointer = child

                alpha = max(alpha, value)
                if alpha <= beta:
                    break #beta cutoff
            return value, pointer

    def eval_board(self,board):
        return random.randint(-1000,1000)

    def close(self):
        pass

    def request (self):
        print("Nathan requested to go fuck himself")
        return []