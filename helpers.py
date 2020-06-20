import chess
import random
import re

class methods():

    def __init__(self):
        """
        compiles the text parser for generating move lists
        """
        self.parser = re.compile(r"(?:\w|\+|\#|\=|\-){2,6}(?=,|\))")

    def getLegalMoveList(self, board):
        """
        Gets a list of all legal moves for a board
        """
        leg_move = str(board.legal_moves)
        list = re.findall(self.parser ,leg_move)
        for i in range(len(list)):
            try:
                list[i] = board.parse_san(list[i])
            except:
                print("proposed move failed parse: " + str(list[i]))
        return list


    # def getLegalMoveset(self, board):
    #     """
    #     Gets a list of all legal moves for a board2
    #     """
    #     leg_move = str(board.legal_moves)
    #     list = re.findall(self.parser ,leg_move)
    #     return list    

    # @staticmethod
    # def boardToListList(board):
    #     fen = str(board.fen())
    #     fen = re.sub(r" .+",'', fen)
    #     tar = ""
    #     for i in range(1, 9):
    #         tar += "0"
    #         fen = fen.replace(str(i), tar)
    #     fen = fen.split("/")
    #     return fen


