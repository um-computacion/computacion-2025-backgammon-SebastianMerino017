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
        