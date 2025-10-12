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
    
    def has_pieces_in_home_board(self, color):
        if color == "white":
            home_range = range(18, 24)
        else:
            home_range = range(0, 6)
        
        for pos in home_range:
            if self.__board__.__pos__[pos] is not None:
                if self.__board__.__pos__[pos][0] == color:
                    return True
        
        if self.__board__.__bar__[color] == 0:
            for pos in range(24):
                if pos not in home_range:
                    if self.__board__.__pos__[pos] is not None:
                        if self.__board__.__pos__[pos][0] == color:
                            return False
            return True
        return False
    
    def validate_move_distance(self, from_pos, to_pos, color):
        if color == "white":
            distance = to_pos - from_pos
        else:
            distance = from_pos - to_pos
        
        available = self.__dice__.get_available_values()
        return distance in available
    
    def move_piece(self, from_pos, to_pos):
        current = self.get_current_player()
        
        if not current.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {current.name}")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("No hay dados disponibles para mover")
        
        if self.must_enter_from_bar():
            raise InvalidMoveError("Debes entrar fichas desde la barra primero")
        
        if not self.__board__.is_valid_position(from_pos) or not self.__board__.is_valid_position(to_pos):
            raise InvalidMoveError("Posición inválida")
        
        if not self.validate_move_distance(from_pos, to_pos, current.color):
            raise InvalidMoveError("La distancia no corresponde a los dados disponibles")
        
        if current.color == "white":
            distance = to_pos - from_pos
        else:
            distance = from_pos - to_pos
        
        success = self.__board__.move_piece(from_pos, to_pos, current.color)
        
        if not success:
            raise InvalidMoveError("Movimiento inválido")
        
        self.__dice__.use_value(distance)
        
        return True
    
    def enter_from_bar(self, to_pos):
        current = self.get_current_player()
        
        if not current.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {current.name}")
        
        if not self.must_enter_from_bar():
            raise NoPiecesInBarError("No tienes fichas en la barra")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("No hay dados disponibles")
        
        if current.color == "white":
            entry_zone = range(18, 24)
            bar_position = 24
        else:
            entry_zone = range(0, 6)
            bar_position = -1

        if to_pos not in entry_zone:
            raise InvalidMoveError(f"Debes entrar en tu zona de entrada")
        
        if current.color == "white":
            distance = to_pos - bar_position
        else:
            distance = bar_position - to_pos
        
        distance = abs(distance)
        
        if distance not in self.__dice__.get_available_values():
            raise InvalidMoveError("La distancia no corresponde a los dados disponibles")
        
        success = self.__board__.enter_from_bar(to_pos, current.color)
        
        if not success:
            raise InvalidMoveError("No se puede entrar en esa posición")
        
        self.__dice__.use_value(distance)
        
        return True
    
    def bear_off(self, from_pos):
        current = self.get_current_player()
        
        if not current.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {current.name}")
        
        if self.must_enter_from_bar():
            raise InvalidMoveError("Debes entrar fichas desde la barra primero")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("No hay dados disponibles")
        
        if not self.has_pieces_in_home_board(current.color):
            raise InvalidMoveError("No todas tus fichas están en el home board")
        
        if current.color == "white":
            if not (18 <= from_pos <= 23):
                raise InvalidMoveError("Solo puedes sacar fichas desde tu home board")
            distance = 24 - from_pos
        else:
            if not (0 <= from_pos <= 5):
                raise InvalidMoveError("Solo puedes sacar fichas desde tu home board")
            distance = from_pos + 1
        
        available = self.__dice__.get_available_values()
        
        can_bear_off_exact = distance in available
        can_bear_off_higher = any(d > distance for d in available)
        
        if not (can_bear_off_exact or can_bear_off_higher):
            raise InvalidMoveError("No tienes un dado válido para sacar esta ficha")
        
        success = self.__board__.bear_off(from_pos, current.color)
        
        if not success:
            raise InvalidMoveError("No se puede sacar la ficha")
        
        if can_bear_off_exact:
            self.__dice__.use_value(distance)
        else:
            for d in sorted(available, reverse=True):
                if d > distance:
                    self.__dice__.use_value(d)
                    break
        
        Player.game_pieces[current.color]['on_board'] -= 1
        Player.game_pieces[current.color]['off_board'] += 1
           