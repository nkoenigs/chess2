import chess
import random
import helpers

import multiprocessing as mp

class engine:
    # needs initializer
    def __init__(self, tlim):
        pass
    
    def play(self, board, tlim):
        help = helpers.methods()
        list = help.getLegalMoveList(board)
        index = random.randint(0, len(list) - 1)
        optimal_play = list[index]
        return optimal_play

    def close(self):
        pass

    def request(self):
        return []