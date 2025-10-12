import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.cli import BackgammonCLI
from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.player import Player


class TestBackgammonCLI(unittest.TestCase):
    
    def setUp(self):
        self.cli = BackgammonCLI()
        Player.reset_game()
    
    def tearDown(self):
        Player.reset_game()
    
    def test_initialization(self):
        self.assertIsNone(self.cli.__game__)
        self.assertFalse(self.cli.__running__)
    
    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        with patch('os.name', 'nt'):
            self.cli.clear_screen()
            mock_system.assert_called_once_with('cls')