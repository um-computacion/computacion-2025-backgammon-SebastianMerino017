import sys
import os

# Importar las clases del juego
from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.board import Board
from core.dice import Dice
from core.player import Player

class BackgammonCLI:
    def __init__(self):
        self.game = None
        self.running = False
    
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
        
        self.game = Game(player1_name, player2_name)
        self.game.start()
        
        print(f"\n¡Juego creado! {player1_name} (Blanco) vs {player2_name} (Negro)")
        input("\nPresiona Enter para comenzar...")
    
    def display_game_state(self):
        """Mostrar el estado actual del juego"""
        current_player = self.game.get_current_player()
        dice = self.game.get_dice()
        board = self.game.get_board()

        print(f"Turno actual: {current_player.name} ({current_player.color})")
        print(f"Dados: {dice}")
        
    
        pieces_info = Player.game_pieces
        print(f"Fichas en tablero - Blanco: {pieces_info['white']['on_board']}, Negro: {pieces_info['black']['on_board']}")
        print(f"Fichas fuera - Blanco: {pieces_info['white']['off_board']}, Negro: {pieces_info['black']['off_board']}")
        
        print()
        board.display_board_console()
        print()

    def show_available_moves(self):
        dice = self.game.get_dice()
        available_values = dice.get_available_values()
        
        if available_values:
            print(f"Dados disponibles: {available_values}")
        else:
            print("No hay dados disponibles - termina tu turno")
        
        if self.game.must_enter_from_bar():
            current_player = self.game.get_current_player()
            print(f"ATENCION: Tienes {self.game.get_board().__bar__[current_player.color]} ficha(s) en la barra que deben entrar primero")
        
        if self.game.can_bear_off():
            print("Puedes comenzar a sacar fichas")

    def handle_dice_roll(self):
        
        try:
            dice_result = self.game.roll_dice()
            if dice_result:
                print(f"{self.game.get_current_player().name} tiro: {dice_result}")
                if self.game.get_dice().is_double():
                    print("DOBLE! Tienes 4 movimientos disponibles")
            else:
                print("Error al tirar los dados")
        except NotYourTurnError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        