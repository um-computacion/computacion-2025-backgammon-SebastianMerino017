import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.cli import CLI
from core.game import Game, InvalidMoveError, NotYourTurnError
from core.player import Player

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.mock_game.is_game_over.return_value = False
        
        self.mock_player = MagicMock(spec=Player)
        self.mock_player.name = "Jugador 1"
        self.mock_player.color = "white"
        
        self.mock_game.get_current_player.side_effect = None
        self.mock_game.get_current_player.return_value = self.mock_player
        
        self.cli = CLI()
        self.cli.__game__ = self.mock_game

        self.cli.clear_screen = MagicMock()
        self.cli.print_header = MagicMock()
        self.cli.print_board = MagicMock()
        self.cli.print_dice = MagicMock()
        self.cli.print_game_info = MagicMock()
        self.cli.show_help = MagicMock()
        self.cli.handle_dice_roll = MagicMock()
        self.cli.handle_move_piece = MagicMock()
        self.cli.handle_end_turn = MagicMock()
        self.cli.handle_bear_off = MagicMock()
        self.cli.handle_enter_from_bar = MagicMock()
        self.cli.show_game_status = MagicMock()
        self.cli.show_available_moves = MagicMock()


    @patch('builtins.input', side_effect=["Jugador Test 1", "Jugador Test 2", "ENTER"])
    @patch('builtins.print')
    @patch('cli.cli.Game', return_value=MagicMock(spec=Game))
    def test_setup_game_names(self, mock_game_class, mock_print, mock_input):
        cli = CLI()
        cli.clear_screen = MagicMock()
        cli.print_header = MagicMock()
        cli.setup_game()
        
        self.assertEqual(mock_input.call_count, 3)
        mock_game_class.assert_called_once_with("Jugador Test 1", "Jugador Test 2")
        cli.__game__.start.assert_called_once()
        mock_print.assert_any_call(f"\n¡Juego creado! {cli.__game__.get_players()[0]} (white) vs {cli.__game__.get_players()[1]} (black)")

    @patch('builtins.input', side_effect=["", "", "ENTER"])
    @patch('builtins.print')
    @patch('cli.cli.Game', return_value=MagicMock(spec=Game))
    def test_setup_game_default_names(self, mock_game_class, mock_print, mock_input):
        cli = CLI()
        cli.clear_screen = MagicMock()
        cli.print_header = MagicMock()
        cli.setup_game()
        
        self.assertEqual(mock_input.call_count, 3)
        mock_game_class.assert_called_once_with("Jugador 1", "Jugador 2")

    @patch('builtins.input', side_effect=['r', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_roll_dice(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.handle_dice_roll.assert_called_once()
        self.assertEqual(self.cli.print_board.call_count, 2)

    @patch('builtins.input', side_effect=['m', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_move_piece(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.handle_move_piece.assert_called_once()
        self.assertEqual(self.cli.print_board.call_count, 2)
        
    @patch('builtins.input', side_effect=['e', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_end_turn(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.handle_end_turn.assert_called_once()
        self.assertEqual(self.cli.print_board.call_count, 2)

    @patch('builtins.input', side_effect=['h', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_help(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.show_help.assert_called_once()
        self.assertEqual(self.cli.print_board.call_count, 2)

    @patch('builtins.input', side_effect=['x', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_invalid_option(self, mock_print, mock_input):
        self.cli.main_menu()
        mock_print.assert_any_call("Opcion no valida. Presiona 'h' para ver la ayuda.")
        self.assertEqual(self.cli.print_board.call_count, 2)
    
    @patch('builtins.input', side_effect=['b', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_bar(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.handle_enter_from_bar.assert_called_once()
    
    @patch('builtins.input', side_effect=['s', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_bear_off(self, mock_print, mock_input):
        self.cli.handle_bear_off.return_value = "ok"
        self.cli.main_menu()
        self.cli.handle_bear_off.assert_called_once()

    @patch('builtins.input', side_effect=['i', 'ENTER', 'q', 's'])
    @patch('builtins.print')
    def test_main_menu_status(self, mock_print, mock_input):
        self.cli.main_menu()
        self.cli.show_game_status.assert_called_once()

    @patch('builtins.print')
    @patch('os.system')
    def test_run_normal_flow(self, mock_os, mock_print):
        self.cli.setup_game = MagicMock()
        self.cli.main_menu = MagicMock()
        
        self.cli.run()
        
        mock_print.assert_any_call(" " * 15 + "Bienvenido a Backgammon CLI!")
        self.cli.setup_game.assert_called_once()
        self.cli.main_menu.assert_called_once()

    @patch('builtins.print')
    @patch('os.system')
    def test_run_keyboard_interrupt(self, mock_os, mock_print):
        self.cli.setup_game = MagicMock(side_effect=KeyboardInterrupt)
        
        self.cli.run()
        
        mock_print.assert_any_call("\n\n¡Juego interrumpido! Hasta luego.")

    @patch('builtins.print')
    @patch('os.system')
    def test_run_generic_exception(self, mock_os, mock_print):
        self.cli.setup_game = MagicMock(side_effect=Exception("Error critico"))
        
        self.cli.run()
        
        mock_print.assert_any_call("\nError critico: Error critico")

if __name__ == '__main__':
    unittest.main()