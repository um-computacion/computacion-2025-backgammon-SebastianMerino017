import unittest
from unittest.mock import patch, MagicMock

from cli.cli import CLI


class TestCLIExtraPaths(unittest.TestCase):

    @patch('builtins.print')
    def test_setup_game_with_empty_names_uses_defaults(self, mock_print):
        cli = CLI()
        # Patch the Game class used inside cli to avoid heavy initialization
        with patch('cli.cli.Game') as MockGame:
            mock_game = MagicMock()
            mock_game.get_players.return_value = ['Jugador 1', 'Jugador 2']
            MockGame.return_value = mock_game

            with patch('builtins.input', side_effect=['', '']):
                cli.setup_game()

        # ensure game was created and start() was called on the mocked Game
        MockGame.assert_called_once()
        mock_game.start.assert_called()

    @patch('builtins.print')
    def test_show_available_moves_various_warnings(self, mock_print):
        cli = CLI()
        gm = MagicMock()
        dice = MagicMock()
        dice.get_available_values.return_value = [3]
        gm.get_dice.return_value = dice
        gm.must_enter_from_bar.return_value = True
        gm.can_bear_off.return_value = True
        mock_player = MagicMock()
        mock_player.color = 'white'
        gm.get_current_player.return_value = mock_player
        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 2, 'black': 0}}
        gm.get_board.return_value = board
        cli.__game__ = gm

        cli.show_available_moves()

        mock_print.assert_any_call('Dados disponibles: [3]')
        mock_print.assert_any_call('ATENCION: Tienes 2 ficha(s) en la barra que deben entrar primero')
        mock_print.assert_any_call('Puedes comenzar a sacar fichas del tablero')

    @patch('builtins.print')
    def test_handle_move_piece_capture_message(self, mock_print):
        cli = CLI()
        gm = MagicMock()
        gm.move_piece.return_value = True
        mock_player = MagicMock()
        mock_player.color = 'white'
        gm.get_current_player.return_value = mock_player
        board = MagicMock()
        # enemy (black) has a piece in bar after the move
        board.get_state.return_value = {'bar': {'white': 0, 'black': 1}}
        gm.get_board.return_value = board
        cli.__game__ = gm

        with patch('builtins.input', side_effect=['1', '2']):
            cli.handle_move_piece()

        mock_print.assert_any_call('¡Capturaste una ficha enemiga!')

    @patch('builtins.print')
    def test_handle_enter_from_bar_raises_and_prints(self, mock_print):
        cli = CLI()
        gm = MagicMock()
        mock_player = MagicMock()
        mock_player.color = 'white'
        gm.get_current_player.return_value = mock_player
        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 1, 'black': 0}}
        gm.get_board.return_value = board
        # Simulate game raising NoPiecesInBarError when trying to enter
        gm.enter_from_bar.side_effect = Exception('boom')
        cli.__game__ = gm

        with patch('builtins.input', side_effect=['19']):
            cli.handle_enter_from_bar()

        mock_print.assert_any_call('Error inesperado: boom')

    @patch('builtins.print')
    def test_handle_bear_off_game_over_prints_winner(self, mock_print):
        cli = CLI()
        gm = MagicMock()
        mock_player = MagicMock()
        mock_player.color = 'white'
        gm.get_current_player.return_value = mock_player
        gm.bear_off.return_value = True
        gm.is_game_over.return_value = True
        winner = MagicMock()
        winner.name = 'Campeon'
        gm.get_winner.return_value = winner
        cli.__game__ = gm

        with patch('builtins.input', side_effect=['24']):
            res = cli.handle_bear_off()

        mock_print.assert_any_call("¡¡¡ CAMPEON HA GANADO EL JUEGO !!!")
        self.assertEqual(res, 'game_over')

    @patch('builtins.print')
    def test_main_menu_calls_show_game_status_on_i(self, mock_print):
        cli = CLI()
        gm = MagicMock()
        gm.is_game_over.return_value = False
        cli.__game__ = gm

        # stub methods to avoid side-effects
        cli.clear_screen = MagicMock()
        cli.print_header = MagicMock()
        cli.print_board = MagicMock()
        cli.print_game_info = MagicMock()
        cli.show_game_status = MagicMock()

        seq = ['i', 'q', 's']
        with patch('builtins.input', side_effect=seq):
            cli.main_menu()

        cli.show_game_status.assert_called()


if __name__ == '__main__':
    unittest.main()
