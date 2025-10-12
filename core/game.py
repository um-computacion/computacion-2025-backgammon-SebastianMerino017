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
    
    def get_current_player(self):
        return self.__current_player__
    
    def get_board(self):
        return self.__board__
    
    def get_dice(self):
        return self.__dice__
    
    def get_players(self):
        return (self.__player1__, self.__player2__)
    
    def roll_dice(self):
        if not self.__game_started__:
            return None
        
        current = self.get_current_player()
        if not current.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {current.name}")
        
        result = self.__dice__.roll()
        return result
    
    def get_available_moves(self):
        return self.__dice__.get_available_values()
    
    def must_enter_from_bar(self):
        current = self.get_current_player()
        return self.__board__.__bar__[current.color] > 0
    
    def can_bear_off(self):
        current = self.get_current_player()
        return self.__board__.has_pieces_in_home_board(current.color)