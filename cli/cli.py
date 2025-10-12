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
        """Limpiar la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')