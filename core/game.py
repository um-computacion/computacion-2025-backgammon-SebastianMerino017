from core.board import Board
from core.dice import Dice
from core.player import Player

class InvalidMoveError(Exception):
    pass

class NotYourTurnError(Exception):
    pass

class NoPiecesInBarError(Exception):
    pass

class Game:
    def __init__(self, player1_name: str, player2_name: str):
        self.__player1__ = Player(player1_name, "white")
        self.__player2__ = Player(player2_name, "black")
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__current_player__ = self.__player1__
        self.__game_started__ = False
        self.__winner__ = None
        self.__dice_rolled__ = False

    def start(self):
        self.__game_started__ = True
        self.__dice__ = Dice()
        self.__current_player__ = self.__player1__
        self.__dice_rolled__ = False
        return True

    def get_board(self):
        return self.__board__

    def get_current_player(self):
        return self.__current_player__
    
    def get_dice(self):
        return self.__dice__
    
    def get_players(self):
        return [self.__player1__, self.__player2__]
    
    def get_winner(self):
        return self.__winner__
    
    def is_game_over(self):
        state = self.__board__.get_state()
        pieces_info = Player.game_pieces
        
        if pieces_info['white']['off_board'] == 15:
            self.__winner__ = self.__player1__
            return True
        if pieces_info['black']['off_board'] == 15:
            self.__winner__ = self.__player2__
            return True
        
        return False

    def get_game_state(self):
        pieces_info = Player.game_pieces
        return {
            "board": self.__board__.get_state(),
            "dice": self.__dice__.get_values(),
            "current_player": self.__current_player__.color,
            "started": self.__game_started__,
            "player1": {
                "name": self.__player1__.name,
                "color": self.__player1__.color,
                "pieces": pieces_info['white']
            },
            "player2": {
                "name": self.__player2__.name,
                "color": self.__player2__.color,
                "pieces": pieces_info['black']
            }
        }

    def roll_dice(self):
        if not self.__game_started__:
            return None
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        if self.__dice__.has_available_values():
            raise InvalidMoveError("Ya has tirado los dados en este turno.")
        result = self.__dice__.roll()
        self.__dice_rolled__ = True
        return result

    def move_piece(self, from_point, to_point):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        if not isinstance(from_point, int) or not isinstance(to_point, int):
            raise InvalidMoveError("Las posiciones deben ser números enteros.")
        if from_point < 0 or from_point > 23 or to_point < 0 or to_point > 23:
            raise InvalidMoveError("Posiciones fuera del rango del tablero (0-23).")
        
        state = self.__board__.get_state()
        if state["bar"][self.__current_player__.color] > 0:
            raise InvalidMoveError("Debes reingresar tus fichas del bar antes de mover otras.")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("Debes tirar los dados primero.")
        
        distance = abs(to_point - from_point)
        if distance not in self.__dice__.get_available_values():
            raise InvalidMoveError(f"No puedes mover {distance} espacios con los dados actuales.")
        
        if self.__current_player__.color == "white" and to_point < from_point:
            raise InvalidMoveError("Dirección incorrecta para las fichas blancas.")
        if self.__current_player__.color == "black" and to_point > from_point:
            raise InvalidMoveError("Dirección incorrecta para las fichas negras.")
        
        if not self.__board__.is_valid_move(self.__current_player__.color, from_point, to_point):
            raise InvalidMoveError("Movimiento inválido según el estado del tablero.")
        
        self.__board__.move_piece(self.__current_player__.color, from_point, to_point)
        self.__dice__.use_value(distance)
        return True

    def must_enter_from_bar(self):
        state = self.__board__.get_state()
        return state["bar"][self.__current_player__.color] > 0
    
    def can_bear_off(self):
        pieces_info = Player.game_pieces
        color_pieces = pieces_info[self.__current_player__.color]
        
        state = self.__board__.get_state()
        if state["bar"][self.__current_player__.color] > 0:
            return False
        
        return True
    
    def enter_from_bar(self, to_point):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        
        state = self.__board__.get_state()
        if state["bar"][self.__current_player__.color] == 0:
            raise NoPiecesInBarError("No tienes fichas en la barra.")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("Debes tirar los dados primero.")
        return True
    
    def bear_off(self, from_point):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        
        if not self.can_bear_off():
            raise InvalidMoveError("No puedes sacar fichas aún.")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("Debes tirar los dados primero.")
        return True

    def end_turn(self):
        if not self.__dice_rolled__:
            raise InvalidMoveError("Debes tirar los dados antes de terminar el turno.")
        
        original_player = self.__current_player__
        
        if not original_player.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {original_player.name}")
            
        if self.__dice__.has_available_values():
            raise InvalidMoveError("Aún tienes dados por usar.")
        
        Player.switch_turn()
        self.__current_player__ = (
            self.__player2__ if original_player == self.__player1__ else self.__player1__
        )
        self.__dice__ = Dice()
        self.__dice_rolled__ = False
        return True

    def __str__(self):
        state = "Iniciado" if self.__game_started__ else "No iniciado"
        return f"Juego de Backgammon ({state}) - Turno: {self.__current_player__.name}"