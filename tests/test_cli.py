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

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_available_moves_no_dice(self, mock_stdout):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.show_available_moves()
        output = mock_stdout.getvalue()
        self.assertIn("termina tu turno", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint', side_effect=[3, 5])
    def test_handle_dice_roll_valid(self, mock_randint, mock_stdout):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.handle_dice_roll()
        output = mock_stdout.getvalue()
        self.assertIn("tiro", output.lower())
    
    @patch('builtins.input', side_effect=['1', '4'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint', side_effect=[3, 5])
    def test_handle_move_piece_valid(self, mock_randint, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli._BackgammonCLI__game__.roll_dice()
        board = self.cli._BackgammonCLI__game__.get_board()
        board._Board__pos__[0] = ["white", 2]
        board._Board__pos__[3] = None
        self.cli.handle_move_piece()
        output = mock_stdout.getvalue()
        self.assertIn("exitosamente", output.lower())
    
    @patch('builtins.input', side_effect=['abc', 'xyz'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_move_piece_invalid_input(self, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.handle_move_piece()
        output = mock_stdout.getvalue()
        self.assertIn("Error", output)
    
    @patch('builtins.input', side_effect=['0', '25'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_move_piece_out_of_range(self, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.handle_move_piece()
        output = mock_stdout.getvalue()
        self.assertIn("Error", output)
    
    @patch('builtins.input', return_value='20')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint', side_effect=[3, 5])
    def test_handle_enter_from_bar_valid(self, mock_randint, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli._BackgammonCLI__game__.roll_dice()
        board = self.cli._BackgammonCLI__game__.get_board()
        board._Board__bar__["white"] = 1
        board._Board__pos__[19] = None
        self.cli.handle_enter_from_bar()
        output = mock_stdout.getvalue()
        self.assertIn("exitosamente", output.lower())
    
    @patch('builtins.input', return_value='abc')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_enter_from_bar_invalid_input(self, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        board = self.cli._BackgammonCLI__game__.get_board()
        board._Board__bar__["white"] = 1
        self.cli.handle_enter_from_bar()
        output = mock_stdout.getvalue()
        self.assertIn("Error", output)

    @patch('builtins.input', return_value='20')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint', side_effect=[6, 6])
    def test_handle_bear_off_valid(self, mock_randint, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli._BackgammonCLI__game__.roll_dice()
        board = self.cli._BackgammonCLI__game__.get_board()
        board._Board__pos__ = [None for _ in range(24)]
        board._Board__pos__[19] = ["white", 2]
        board._Board__bar__["white"] = 0
        Player.game_pieces["white"]["on_board"] = 2
        self.cli.handle_bear_off()
        output = mock_stdout.getvalue()
        self.assertIn("exitosamente", output.lower())
    
    @patch('builtins.input', return_value='abc')
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_bear_off_invalid_input(self, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.handle_bear_off()
        output = mock_stdout.getvalue()
        self.assertIn("Error", output)
    
    @patch('builtins.input', return_value='s')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.randint', side_effect=[3, 5])
    def test_handle_end_turn_with_dice(self, mock_randint, mock_stdout, mock_input):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli._BackgammonCLI__game__.roll_dice()
        self.cli.handle_end_turn()
        output = mock_stdout.getvalue()
        self.assertIn("terminado", output.lower())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_handle_end_turn_no_dice(self, mock_stdout):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.handle_end_turn()
        output = mock_stdout.getvalue()
        self.assertIn("terminado", output.lower())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_help(self, mock_stdout):
        self.cli.show_help()
        output = mock_stdout.getvalue()
        self.assertIn("AYUDA", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_game_status(self, mock_stdout):
        self.cli._BackgammonCLI__game__ = Game("Test1", "Test2")
        self.cli._BackgammonCLI__game__.start()
        self.cli.show_game_status()
        output = mock_stdout.getvalue()
        self.assertIn("ESTADO", output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    
