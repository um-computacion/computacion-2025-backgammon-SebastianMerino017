import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.cli import BackgammonCLI
from core.game import Game, InvalidMoveError, NotYourTurnError
from core.player import Player

class TestBackgammonCLI(unittest.TestCase):

    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.mock_game.is_game_over.return_value = False
        
        self.mock_player = MagicMock(spec=Player)
        self.mock_player.name = "Jugador 1"
        self.mock_player.color = "white"
        
        self.mock_game.get_current_player.side_effect = None
        self.mock_game.get_current_player.return_value = self.mock_player
        
        self.cli = BackgammonCLI()
        self.cli.__game__ = self.mock_game

    @patch('builtins.input', side_effect=["Jugador Test 1", "Jugador Test 2"])
    @patch('builtins.print')
    @patch('cli.cli.Game', return_value=MagicMock(spec=Game))
    @patch('os.system')
    def test_setup_game_names(self, mock_os, mock_game_class, mock_print, mock_input):
        cli = BackgammonCLI() 
        cli.setup_game()
        
        self.assertEqual(mock_input.call_count, 2)
        mock_game_class.assert_called_once_with("Jugador Test 1", "Jugador Test 2")
        cli.__game__.start.assert_called_once()
        mock_print.assert_called_with("\n¡Juego creado! Jugador Test 1 (white) vs Jugador Test 2 (black)")

    @patch('builtins.input', side_effect=["", ""])
    @patch('builtins.print')
    @patch('cli.cli.Game', return_value=MagicMock(spec=Game))
    @patch('os.system')
    def test_setup_game_default_names(self, mock_os, mock_game_class, mock_print, mock_input):
        cli = BackgammonCLI()
        cli.setup_game()
        
        self.assertEqual(mock_input.call_count, 2)
        mock_game_class.assert_called_once_with("Jugador 1", "Jugador 2")

    @patch('builtins.input', side_effect=['r', 'q'])
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_roll_dice(self, mock_os, mock_print, mock_input):
        self.mock_game.roll_dice.return_value = (3, 5)
        
        self.cli.main_menu()
        
        self.mock_game.roll_dice.assert_called_once()
        mock_print.assert_any_call("\n¡Dados tirados! Resultado: (3, 5)")

    @patch('builtins.input', side_effect=['r', 'q']) 
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_roll_dice_error(self, mock_os, mock_print, mock_input):
        self.mock_game.roll_dice.side_effect = InvalidMoveError("Ya has tirado los dados.")
        
        self.cli.main_menu()
        
        self.mock_game.roll_dice.assert_called_once()
        mock_print.assert_any_call("\nError: Ya has tirado los dados.")

    @patch('builtins.input', side_effect=['m', '0', '5', 'q'])
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_move_piece(self, mock_os, mock_print, mock_input):
        self.mock_game.move_piece.return_value = True
        
        self.cli.main_menu()
        
        self.mock_game.move_piece.assert_called_once_with(0, 5)
        mock_print.assert_any_call("\nMovimiento exitoso: 0 -> 5")
        
    @patch('builtins.input', side_effect=['m', '0', '99', 'q']) 
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_move_piece_error(self, mock_os, mock_print, mock_input):
        self.mock_game.move_piece.side_effect = InvalidMoveError("Dado no disponible.")
        
        self.cli.main_menu()
        
        self.mock_game.move_piece.assert_called_once_with(0, 99)
        mock_print.assert_any_call("\nError: Dado no disponible.")

    @patch('builtins.input', side_effect=['e', 'q'])
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_end_turn(self, mock_os, mock_print, mock_input):
        mock_player_2 = MagicMock(spec=Player, name="Jugador 2", color="black")
        
        self.mock_game.get_current_player.side_effect = [
            self.mock_player,
            self.mock_player,
            mock_player_2,
            mock_player_2
        ]
        
        self.cli.main_menu()
        
        self.mock_game.end_turn.assert_called_once()
        mock_print.assert_any_call("\nTurno finalizado. Ahora juega Jugador 2 (black).")

    @patch('builtins.input', side_effect=['h', 'q'])
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_help(self, mock_os, mock_print, mock_input):
        self.cli.main_menu()
        
        mock_print.assert_any_call("--- AYUDA ---")
        mock_print.assert_any_call("  [h] Ayuda: Muestra este menú.")

    @patch('builtins.input', side_effect=['x', 'q'])
    @patch('builtins.print')
    @patch('os.system')
    def test_main_menu_invalid_option(self, mock_os, mock_print, mock_input):
        self.cli.main_menu()
        
        mock_print.assert_any_call("Opcion no valida. Presiona 'h' para ver la ayuda.")

    @patch('cli.cli.BackgammonCLI.main_menu')
    @patch('cli.cli.BackgammonCLI.setup_game')
    @patch('builtins.print')
    @patch('os.system')
    def test_run_normal_flow(self, mock_os, mock_print, mock_setup, mock_menu):
        self.cli.run()
        mock_print.assert_any_call(" " * 15 + "Bienvenido a Backgammon CLI!")
        mock_setup.assert_called_once()
        mock_menu.assert_called_once()

    @patch('cli.cli.BackgammonCLI.setup_game', side_effect=KeyboardInterrupt)
    @patch('builtins.print')
    @patch('os.system')
    def test_run_keyboard_interrupt(self, mock_os, mock_print, mock_setup):
        self.cli.run()
        
        mock_print.assert_any_call("\n\n¡Juego interrumpido! Hasta luego.")

    @patch('cli.cli.BackgammonCLI.setup_game', side_effect=Exception("Error critico"))
    @patch('builtins.print')
    @patch('os.system')
    def test_run_generic_exception(self, mock_os, mock_print, mock_setup):
        self.cli.run()
        
        mock_print.assert_any_call("\nError critico: Error critico")

if __name__ == '__main__':
    unittest.main()