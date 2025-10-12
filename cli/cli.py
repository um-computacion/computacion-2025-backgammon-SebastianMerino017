import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.board import Board
from core.dice import Dice
from core.player import Player


class BackgammonCLI:
    def __init__(self):
        self.__game__ = None
        self.__running__ = False
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        print("=" * 60)
        print("           BACKGAMMON - JUEGO DE TABLERO")
        print("=" * 60)
        print()
    
    def setup_game(self):
        self.clear_screen()
        self.print_header()
        
        print("CONFIGURACION DEL JUEGO")
        print("-" * 30)
        
        player1_name = input("Nombre del Jugador 1 (Blanco): ").strip()
        player2_name = input("Nombre del Jugador 2 (Negro): ").strip()
        
        if not player1_name:
            player1_name = "Jugador 1"
        if not player2_name:
            player2_name = "Jugador 2"
        
        self.__game__ = Game(player1_name, player2_name)
        self.__game__.start()
        
        print(f"\n¡Juego creado! {player1_name} (Blanco) vs {player2_name} (Negro)")
        input("\nPresiona Enter para comenzar...")
    
    def display_game_state(self):
        current_player = self.__game__.get_current_player()
        dice = self.__game__.get_dice()
        board = self.__game__.get_board()
        
        print(f"Turno actual: {current_player.name} ({current_player.color})")
        print(f"Dados: {dice}")
        
        pieces_info = Player.game_pieces
        print(f"Fichas en tablero - Blanco: {pieces_info['white']['on_board']}, Negro: {pieces_info['black']['on_board']}")
        print(f"Fichas fuera - Blanco: {pieces_info['white']['off_board']}, Negro: {pieces_info['black']['off_board']}")
        
        print()
        board.display_board_console()
        print()
    
    def show_available_moves(self):
        dice = self.__game__.get_dice()
        available_values = dice.get_available_values()
        
        if available_values:
            print(f"Dados disponibles: {available_values}")
        else:
            print("No hay dados disponibles - termina tu turno")
        
        if self.__game__.must_enter_from_bar():
            current_player = self.__game__.get_current_player()
            bar_count = self.__game__.get_board().__bar__[current_player.color]
            print(f"ATENCION: Tienes {bar_count} ficha(s) en la barra que deben entrar primero")
        
        if self.__game__.can_bear_off():
            print("Puedes comenzar a sacar fichas del tablero")
    
    def handle_dice_roll(self):
        try:
            dice_result = self.__game__.roll_dice()
            if dice_result:
                print(f"\n{self.__game__.get_current_player().name} tiro: {dice_result}")
                if self.__game__.get_dice().is_double():
                    print("¡DOBLE! Tienes 4 movimientos disponibles")
            else:
                print("Error al tirar los dados")
        except NotYourTurnError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    def handle_move_piece(self):
        try:
            print("\nMOVIMIENTO DE FICHA")
            print("-" * 20)
            
            from_pos = input("Posicion de origen (1-24): ").strip()
            to_pos = input("Posicion de destino (1-24): ").strip()
            
            if not from_pos.isdigit() or not to_pos.isdigit():
                print("Error: Las posiciones deben ser numeros")
                return
            
            from_pos = int(from_pos) - 1
            to_pos = int(to_pos) - 1
            
            if not (0 <= from_pos <= 23 and 0 <= to_pos <= 23):
                print("Error: Las posiciones deben estar entre 1 y 24")
                return
            
            success = self.__game__.move_piece(from_pos, to_pos)
            if success:
                print("✓ Movimiento realizado exitosamente")
                
                board = self.__game__.get_board()
                enemy_color = "black" if self.__game__.get_current_player().color == "white" else "white"
                if board.__bar__[enemy_color] > 0:
                    print("¡Capturaste una ficha enemiga!")
                    
        except InvalidMoveError as e:
            print(f"Movimiento invalido: {e}")
        except NotYourTurnError as e:
            print(f"Error de turno: {e}")
        except ValueError:
            print("Error: Ingresa numeros validos")
        except Exception as e:
            print(f"Error inesperado: {e}")
    
 