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
        self.assertIsNone(self.cli._BackgammonCLI__game__)
        self.assertFalse(self.cli._BackgammonCLI__running__)
    
    @patch('os.system')
    def test_clear_screen(self, mock_system):
        self.cli.clear_screen()
        self.assertTrue(mock_system.called)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_header(self, mock_stdout):
        self.cli.print_header()
        output = mock_stdout.getvalue()
        self.assertIn("BACKGAMMON", output)
    
    @patch('builtins.input', side_effect=['Juan', 'Maria', ''])
    @patch('os.system')
    def test_setup_game_with_names(self, mock_system, mock_input):
        self.cli.setup_game()
        players = self.cli._BackgammonCLI__game__.get_players()
        self.assertEqual(players[0].name, "Juan")
        self.assertEqual(players[1].name, "Maria")
    
    @patch('builtins.input', side_effect=['', '', ''])
    @patch('os.system')
    def test_setup_game_default_names(self, mock_system, mock_input):
        self.cli.setup_game()
        players = self.cli._BackgammonCLI__game__.get_players()
        self.assertEqual(players[0].name, "Jugador 1")
        self.assertEqual(players[1].name, "Jugador 2")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_state(self, mock_stdout):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.display_game_state()
        output = mock_stdout.getvalue()
        self.assertIn("Test1", output)
    
