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

#todo warnign
def take_turn(board, engine):
    color = "White"
    if board.turn == chess.BLACK:
        color = "Black"
    start_time = time.clock()
    result = engine.play(board, chess.engine.Limit(time=tlim))
    end_time = time.clock()
    if end_time - start_time > tlim:
        print("went over time by " + str(end_time - start_time - tlim) + " sec")
    if board.uci(result) == "0000":
        print(color + " null")
        return None
    board.push(result)
    debug.write("\n\n" + color + "\n" + board.uci(result) + "\n" + str(board))
    stack.write(board.uci(result)+"\n")
    print(result)
    return board

if __name__ == '__main__':
    tlim = 1

    print("\n\n\n\n\n\n\n")
    white_engine = eng1.engine(tlim)
    black_engine = eng2.engine(tlim)
    engines = {True : white_engine, False: black_engine}

    board = chess.Board()

    while not board.is_game_over():
        temp_board = take_turn(board, engines[board.turn])
        if temp_board == None:
            break
        board = temp_board
        if board.is_game_over():
            break
        if board.turn > 50:
            break

    white_engine.close()
    black_engine.close()

    debug.close()
    stack.close()
    print('\n\nGG!')
    print(str(board.result())+' in '+str(math.ceil(len(board.move_stack)/2))+'\n\n')