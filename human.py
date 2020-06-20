import chess

class engine:
    def __init__(self, tlim):
        pass

    def play(self, board, tlim):
        print(board)
        print('')
        result = input('your move:\n')
        return chess.Move.from_uci(result)