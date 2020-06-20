import chess
import random
import helper

class engine:
    # needs initializer
    def __init__(self):
        self.turn  = 0
    
    def play(self, board, tlim):
        help = helper.meth()
        list = help.getLegalMoveList(board)
        index = random.randint(0, len(list) - 1)
        optimal_play = list[index]
        self.turn += 1
        if self.turn > 101:
            return chess.Move.null()
        return optimal_play