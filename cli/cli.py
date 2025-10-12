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
        