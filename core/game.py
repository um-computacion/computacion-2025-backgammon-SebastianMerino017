from core.board import Board
from core.player import Player
from core.dice import Dice


class InvalidMoveError(Exception):
    pass


class NotYourTurnError(Exception):
    pass


class NoPiecesInBarError(Exception):
    pass


class Game:
    def __init__(self, player1_name, player2_name):
        Player.reset_game()
        
        self.__board__ = Board()
        self.__player1__ = Player(player1_name, "white")
        self.__player2__ = Player(player2_name, "black")
        self.__dice__ = Dice()
        self.__current_player__ = self.__player1__
        self.__winner__ = None
        self.__game_started__ = False
    
    def start(self):
        self.__game_started__ = True
        return True