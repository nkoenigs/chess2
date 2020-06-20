import chess

class engine:
    def __init__(self, tlim):
        pass

    def play(self, board, tlim):
        print(board)
        print('')
        while True:
            result = input('your move:\n')
            try:
                return board.parse_san(result)
            except:
                pass
            