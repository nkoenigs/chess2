import chess
import chess.engine
import math
import time

import RandomEngine as eng1
import RandomEngine as eng2
#import rematch as eng1
# import rematch as eng2

debug = open("game_debug.txt", "w")
stack = open("game_stack.pgn", "w")

tlim = 1

print("\n\n\n\n\n\n\n")
White = eng1.engine(tlim)
Black = eng2.engine(tlim)

board = chess.Board()

while not board.is_game_over():

    start_time = time.clock()
    result = White.play(board, chess.engine.Limit(time=tlim))
    end_time = time.clock()
    if end_time - start_time > tlim:
        print("went over time by " + str(end_time - start_time - tlim) + " sec")
    if board.uci(result) == "0000":
        print("white null")
        break
    board.push(result)
    debug.write("\n\nWhite\n" + board.uci(result) + "\n" + str(board))
    stack.write(board.uci(result)+"\n")
    print(result)

    if board.is_game_over():
        break
    if board.turn > 50:
        break

    start_time = time.clock()
    result = Black.play(board, chess.engine.Limit(time=tlim))
    end_time = time.clock()
    if end_time - start_time > tlim:
        print("went over time by " + str(end_time - start_time - tlim) + " sec")
    if board.uci(result) == "0000":
        print("black null")
        break
    board.push(result)
    debug.write("\n\nBlack\n" + board.uci(result) + "\n" + str(board))
    stack.write(board.uci(result) + "\n")

White.close()
Black.close()

debug.close()
stack.close()
print('\n\nGG!')
print(str(board.result())+' in '+str(math.ceil(len(board.move_stack)/2))+'\n\n')