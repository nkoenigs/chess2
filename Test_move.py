import chess
import chess.engine
import math
import time

import RandomEngine as eng1
#import rematch as eng1

debug = open("game_debug.txt", "w")
stack = open("game_stack.pgn", "w")

print("\n\n\n\n\n\n\n")
White = eng1.engine()

tlim = 1
board = chess.Board()
board.set_fen("r1bqkbnr/ppp1pppp/2np4/8/4P3/5Q2/PPPP1PPP/RNB1KBNR w KQkq -")

while not board.is_game_over():
    result = White.play(board, chess.engine.Limit(time=tlim))
    if board.uci(result) == "0000":
        print("white null")
        break
    print("Whites move = " + str(result))
    board.push(result)
    debug.write("\n\nWhite\n" + board.uci(result) + "\n" + str(board))
    stack.write(board.uci(result)+"\n")

    if board.is_game_over():
        break

    result = input('your move black\n')
    if result == "0000":
        print("black null")
        break
    board.push(chess.Move.from_uci(result))
    debug.write("\n\nBlack\n" + result + "\n" + str(board))
    stack.write(result + "\n")


debug.close()
stack.close()
print('\n\nGG!')
print(str(board.result())+' in '+str(math.ceil(len(board.move_stack)/2))+'\n\n')