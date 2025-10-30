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
        Player.reset_game() # Asegurar que Player se reinicia
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
        # Simplificado para chequear el contador interno de Player
        if Player.game_pieces['white']['off_board'] == 15:
            self.__winner__ = self.__player1__
            return True
        elif Player.game_pieces['black']['off_board'] == 15:
            self.__winner__ = self.__player2__
            return True
        return False
    
    # --- MÉTODO AÑADIDO ---
    def must_enter_from_bar(self):
        """ Verifica si el jugador actual tiene fichas en la barra. """
        color = self.__current_player__.color
        return self.__board__.get_state()['bar'][color] > 0
    # ---

    def roll_dice(self):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        
        current = self.get_current_player()
        if not current.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {current.name}")
        
        if self.__dice_rolled__:
            raise InvalidMoveError("Ya has tirado los dados.")
        
        dice_values = self.__dice__.roll()
        self.__dice_rolled__ = True
        return dice_values

    def move_piece(self, from_point: int, to_point: int):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        
        if not self.__dice_rolled__:
            raise InvalidMoveError("Debes tirar los dados primero.")
        
        if not self.__dice__.has_available_values():
            raise InvalidMoveError("No tienes dados disponibles.")
        
        color = self.__current_player__.color
        
        if self.must_enter_from_bar():
            raise InvalidMoveError("Debes reingresar todas tus piezas de la barra.")

        distance = 0
        if color == "white":
            distance = to_point - from_point
        else:
            distance = from_point - to_point
        
        if distance <= 0:
            raise InvalidMoveError("Movimiento en dirección incorrecta.")
        
        available_dice = self.__dice__.get_available_values()
        
        if distance not in available_dice:
            raise InvalidMoveError("Valor de dado no disponible.")

        if self.__board__.is_valid_move(from_point, to_point, color):
            self.__dice__.use_value(distance)
            return True
        else:
            raise InvalidMoveError("Movimiento inválido (posición bloqueada o no existe).")

    def enter_from_bar(self, to_point: int):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        
        if not self.__dice_rolled__:
            raise InvalidMoveError("Debes tirar los dados primero.")
        
        color = self.__current_player__.color
        
        if not self.must_enter_from_bar():
             raise NoPiecesInBarError("No tienes piezas en la barra.")
        
        dice_value = 0
        if color == "white":
            if not (0 <= to_point <= 5):
                raise InvalidMoveError("Las blancas solo pueden reingresar en [0-5].")
            dice_value = to_point + 1
        else:
            if not (18 <= to_point <= 23):
                raise InvalidMoveError("Las negras solo pueden reingresar en [18-23].")
            dice_value = 24 - to_point
        
        if dice_value not in self.__dice__.get_available_values():
            raise InvalidMoveError("Valor de dado no disponible.")
        
        if self.__board__.is_valid_re_entry(to_point, color):
            self.__dice__.use_value(dice_value)
            return True
        else:
            raise InvalidMoveError("Posición de reingreso bloqueada.")

    def can_bear_off(self):
        color = self.__current_player__.color
        return self.__board__.has_pieces_in_home_board(color)

    def bear_off(self, from_point: int):
        if not self.__game_started__:
            raise InvalidMoveError("El juego no ha iniciado.")
        if not self.__current_player__.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {self.__current_player__.name}")
        
        if not self.can_bear_off():
            raise InvalidMoveError("No puedes sacar fichas aún.")
        
        if not self.__dice_rolled__:
            raise InvalidMoveError("Debes tirar los dados primero.")
        
        if not self.__dice__.has_available_values():
             raise InvalidMoveError("No tienes dados disponibles para bear off.")

        color = self.__current_player__.color
        dice_value_needed = 0
        if color == "white":
            if not (18 <= from_point <= 23):
                 raise InvalidMoveError("Bear off inválido para blancas.")
            dice_value_needed = 24 - from_point
        else: # black
            if not (0 <= from_point <= 5):
                 raise InvalidMoveError("Bear off inválido para negras.")
            dice_value_needed = from_point + 1
            
        available_dice = self.__dice__.get_available_values()
        
        dice_to_use = -1 # Flag to check if a valid die was found
        if dice_value_needed in available_dice:
            dice_to_use = dice_value_needed
        else:
            # Check if a higher die can be used
            higher_dice = sorted([d for d in available_dice if d > dice_value_needed])
            if not higher_dice:
                raise InvalidMoveError("No tienes el dado exacto o uno mayor para sacar.")
                
            # Check if it's the farthest piece
            is_farthest = True
            if color == "white":
                 # Check points 18 to from_point - 1
                 for p in range(18, from_point):
                     pos_state = self.__board__.get_state()['positions'][p]
                     if pos_state and pos_state[0] == color:
                         is_farthest = False
                         break
            else: # black
                 # Check points from_point + 1 to 5
                 for p in range(from_point + 1, 6):
                      pos_state = self.__board__.get_state()['positions'][p]
                      if pos_state and pos_state[0] == color:
                         is_farthest = False
                         break
                         
            if not is_farthest:
                 raise InvalidMoveError("Solo puedes usar un dado mayor si es la pieza más alejada.")
                 
            dice_to_use = higher_dice[0] # Use the smallest available higher die

        if dice_to_use == -1: # Should not happen if logic above is correct
             raise InvalidMoveError("Error lógico al determinar el dado para bear off.")

        if self.__board__.bear_off(from_point, color):
            self.__dice__.use_value(dice_to_use)
            self.__current_player__.bear_off_piece() # Actualizar contador en Player
            if self.is_game_over():
                self.__winner__ = self.__current_player__
            return True
        else:
            # Should not happen if logic is correct, but just in case
            raise InvalidMoveError("Error al intentar sacar la ficha.")


    def end_turn(self):
        original_player = self.__current_player__
        
        if not original_player.is_my_turn():
            raise NotYourTurnError(f"No es el turno de {original_player.name}")
        
        if not self.__dice_rolled__:
            # Permitir pasar si no hay movimientos posibles, incluso sin tirar dados?
            # Por ahora, asumimos que siempre debe tirar dados si es su turno.
            raise InvalidMoveError("Debes tirar los dados antes de terminar el turno.")
            
        if self.__dice__.has_available_values():
            # TODO: Verificar si realmente no hay movimientos posibles
            raise InvalidMoveError("Aún tienes dados por usar.")
        
        original_player.end_turn() # Llama a Player.switch_turn()
        self.__current_player__ = (
            self.__player2__ if original_player == self.__player1__ else self.__player1__
        )
        self.__dice__ = Dice()
        self.__dice_rolled__ = False
        return True

    def get_game_state(self):
        return {
            "board": self.__board__.get_state(),
            "player1": {
                "name": self.__player1__.name,
                "color": self.__player1__.color
            },
            "player2": {
                "name": self.__player2__.name,
                "color": self.__player2__.color
            },
            "current_player": self.__current_player__.name,
            "dice": {
                "values": self.__dice__.get_values(),
                "available": self.__dice__.get_available_values(),
                "is_double": self.__dice__.is_double()
            },
            "winner": self.__winner__.name if self.__winner__ else None,
            "game_started": self.__game_started__
        }

    def __str__(self):
        state = "Iniciado" if self.__game_started__ else "No iniciado"
        return f"Juego de Backgammon ({self.__player1__} vs {self.__player2__}) - {state}"