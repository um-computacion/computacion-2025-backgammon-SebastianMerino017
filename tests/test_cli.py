import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cli.cli import CLI
from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.player import Player


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.mock_game = MagicMock(spec=Game)
        self.mock_game.is_game_over.return_value = False
        self.mock_player = MagicMock(spec=Player)
        self.mock_player.name = "Jugador 1"
        self.mock_player.color = "white"

        self.mock_game.get_current_player.return_value = self.mock_player

        self.cli = CLI()
        self.cli.__game__ = self.mock_game

        # Evitamos limpiar pantalla o loops largos
        self.cli.clear_screen = MagicMock()
        self.cli.print_header = MagicMock()
        self.cli.print_board = MagicMock()
        self.cli.show_available_moves = MagicMock()

    # === NUEVOS TESTS PARA MAYOR COBERTURA ===

    # --- handle_dice_roll ---
    @patch('builtins.print')
    def test_handle_dice_roll_success(self, mock_print):
        self.cli.__game__.roll_dice.return_value = (3, 4)
        self.cli.handle_dice_roll()
        mock_print.assert_any_call("\nJugador 1 tiro: (3, 4)")

    @patch('builtins.print')
    def test_handle_dice_roll_not_your_turn(self, mock_print):
        self.cli.__game__.roll_dice.side_effect = NotYourTurnError("No es tu turno")
        self.cli.handle_dice_roll()
        mock_print.assert_any_call("Error: No es tu turno")

    # --- handle_move_piece ---
    @patch('builtins.input', side_effect=["1", "3"])
    @patch('builtins.print')
    def test_handle_move_piece_success(self, mock_print, mock_input):
        self.cli.__game__.move_piece.return_value = True
        self.cli.handle_move_piece()
        self.cli.__game__.move_piece.assert_called_once_with(0, 2)
        mock_print.assert_any_call("✓ Movimiento realizado exitosamente")

    @patch('builtins.input', side_effect=["a", "3"])
    @patch('builtins.print')
    def test_handle_move_piece_invalid_number(self, mock_print, mock_input):
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Error: Las posiciones deben ser numeros")

    @patch('builtins.input', side_effect=["1", "30"])
    @patch('builtins.print')
    def test_handle_move_piece_out_of_range(self, mock_print, mock_input):
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Error: Las posiciones deben estar entre 1 y 24")

    @patch('builtins.input', side_effect=["1", "2"])
    @patch('builtins.print')
    def test_handle_move_piece_invalid_move(self, mock_print, mock_input):
        self.cli.__game__.move_piece.side_effect = InvalidMoveError("Movimiento no permitido")
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Movimiento invalido: Movimiento no permitido")

    # --- handle_enter_from_bar ---
    @patch('builtins.input', side_effect=["20"])
    @patch('builtins.print')
    def test_handle_enter_from_bar_success_white(self, mock_print, mock_input):
        self.mock_player.color = "white"
        self.mock_game.get_board.return_value.get_state.return_value = {'bar': {'white': 1, 'black': 0}}
        self.cli.__game__.enter_from_bar.return_value = True
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("✓ Ficha entro exitosamente desde la barra")

    @patch('builtins.input', side_effect=["a"])
    @patch('builtins.print')
    def test_handle_enter_from_bar_invalid_number(self, mock_print, mock_input):
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error: La posicion debe ser un numero")

    @patch('builtins.input', side_effect=["25"])
    @patch('builtins.print')
    def test_handle_enter_from_bar_out_of_range(self, mock_print, mock_input):
        self.mock_player.color = "white"
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error: La posicion debe estar entre 19 y 24")

    # --- handle_bear_off ---
    @patch('builtins.input', side_effect=["24"])
    @patch('builtins.print')
    def test_handle_bear_off_success(self, mock_print, mock_input):
        self.mock_player.color = "white"
        self.cli.__game__.bear_off.return_value = True
        self.cli.__game__.is_game_over.return_value = False
        self.cli.handle_bear_off()
        mock_print.assert_any_call("✓ Ficha sacada exitosamente del tablero")

    @patch('builtins.input', side_effect=["x"])
    @patch('builtins.print')
    def test_handle_bear_off_invalid_input(self, mock_print, mock_input):
        self.cli.handle_bear_off()
        mock_print.assert_any_call("Error: La posicion debe ser un numero")

    # --- handle_end_turn ---
    @patch('builtins.input', side_effect=["s"])
    @patch('builtins.print')
    def test_handle_end_turn_success(self, mock_print, mock_input):
        mock_dice = MagicMock()
        mock_dice.get_available_values.return_value = []
        self.cli.__game__.get_dice.return_value = mock_dice
        self.cli.__game__.end_turn.return_value = True
        self.cli.handle_end_turn()
        mock_print.assert_any_call("✓ Turno terminado. Pasando al siguiente jugador...")

    @patch('builtins.input', side_effect=["n"])
    @patch('builtins.print')
    def test_handle_end_turn_not_confirmed(self, mock_print, mock_input):
        mock_dice = MagicMock()
        mock_dice.get_available_values.return_value = [3, 4]
        self.cli.__game__.get_dice.return_value = mock_dice
        self.cli.handle_end_turn()
        mock_print.assert_any_call("Turno no terminado")

    # --- show_help ---
    @patch('builtins.print')
    def test_show_help_prints_commands(self, mock_print):
        self.cli.show_help()
        mock_print.assert_any_call("r  - Tirar dados")
        mock_print.assert_any_call("q  - Salir del juego")

    # --- show_game_status ---
    @patch('builtins.print')
    def test_show_game_status(self, mock_print):
        fake_state = {
            'player1': {'name': 'P1', 'color': 'white', 'pieces': {'on_board': 10, 'off_board': 5}},
            'player2': {'name': 'P2', 'color': 'black', 'pieces': {'on_board': 12, 'off_board': 3}}
        }
        self.cli.__game__.get_game_state.return_value = fake_state
        self.cli.show_game_status()
        mock_print.assert_any_call(f"Jugador 1: P1 (white)")
        mock_print.assert_any_call(f"Jugador 2: P2 (black)")

    class TestCLIExhaustive(unittest.TestCase):

        def setUp(self):
            self.cli = CLI()
            self.mock_game = MagicMock()
        # by default not game over
            self.mock_game.is_game_over.return_value = False
            self.cli.__game__ = self.mock_game
        # avoid clearing screen and header heavy output
            self.cli.clear_screen = MagicMock()
            self.cli.print_header = MagicMock()
            self.cli.print_board = MagicMock()
            self.cli.show_available_moves = MagicMock()

    @patch('builtins.print')
    def test_main_menu_game_over_play_again_yes(self, mock_print):
        # Simulate initial game over, user chooses to play again, then quits
        winner = MagicMock()
        winner.name = 'Winner'
        self.mock_game.get_winner.return_value = winner

        # First loop: game over -> user inputs 's' to play again
        # After setup_game is called, make the game not over and then user quits with 'q'+'s'
        inputs = ['s', 'q', 's']

        # patch setup_game to simply attach the same mock_game (no interactive prompts)
        def fake_setup():
            self.cli.__game__ = self.mock_game

        self.cli.setup_game = fake_setup

        # set first is_game_over True to trigger play again branch, then False
        self.mock_game.is_game_over.side_effect = [True, False]

        with patch('builtins.input', side_effect=inputs):
            self.cli.main_menu()

        mock_print.assert_any_call("\n¡Gracias por jugar!")

    @patch('builtins.print')
    def test_main_menu_many_choices_sequence(self, mock_print):
        # We'll mock handler methods so their internal input calls don't interfere
        self.cli.handle_dice_roll = MagicMock()
        self.cli.handle_move_piece = MagicMock()
        self.cli.handle_enter_from_bar = MagicMock()
        self.cli.handle_bear_off = MagicMock()
        self.cli.handle_end_turn = MagicMock()
        self.cli.show_game_status = MagicMock()
        self.cli.show_help = MagicMock()

        # Sequence of choices; include empty strings for the "Press ENTER to continue" prompts
        seq = [
            'r', '',
            'm', '',
            'b', '',
            's', '',
            'e', '',
            'i', '',
            'h', '',
            'c',
            'z', '',  # invalid option
            'q', 's'  # quit with confirmation
        ]

        with patch('builtins.input', side_effect=seq):
            # ensure game never reports game over during this flow
            self.mock_game.is_game_over.return_value = False
            self.cli.main_menu()

        # verify that our mocks were invoked at least once
        self.cli.handle_dice_roll.assert_called()
        self.cli.handle_move_piece.assert_called()
        self.cli.handle_enter_from_bar.assert_called()
        self.cli.handle_bear_off.assert_called()
        self.cli.handle_end_turn.assert_called()
        self.cli.show_game_status.assert_called()
        self.cli.show_help.assert_called()
        mock_print.assert_any_call("Opcion no valida. Presiona 'h' para ver la ayuda.")

    @patch('builtins.print')
    def test_run_handles_keyboardinterrupt_and_finally(self, mock_print):
        # Make setup_game raise KeyboardInterrupt to hit the KeyboardInterrupt branch
        def raises_keyboard():
            raise KeyboardInterrupt()

        self.cli.setup_game = raises_keyboard
        # run should handle it and set __running__ back to False
        self.cli.run()
        self.assertFalse(self.cli.__running__)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', '2'])
    def test_handle_move_piece_move_raises_valueerror(self, mock_input, mock_print):
        # Simulate a ValueError thrown by move_piece (invalid internal error path)
        self.cli.__game__.move_piece.side_effect = ValueError()
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Error: Ingresa numeros validos")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['Alice', 'Bob', ''])
    def test_setup_game_with_names(self, mock_input, mock_print):
        # Patch Game constructor to return our mock_game and ensure start() is called
        with patch('cli.cli.Game', return_value=self.mock_game):
            self.mock_game.start = MagicMock()
            cli_real = CLI()
            cli_real.clear_screen = MagicMock()
            cli_real.setup_game()
            self.assertIs(cli_real.__game__, self.mock_game)
            # ensure start was called on the created game
            self.mock_game.start.assert_called()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['3'])
    def test_handle_enter_from_bar_black(self, mock_input, mock_print):
        # Test the black-player branch of enter_from_bar (valid_range 1-6)
        player = MagicMock()
        player.color = 'black'
        self.cli.__game__.get_current_player.return_value = player
        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 0, 'black': 1}}
        self.cli.__game__.get_board.return_value = board
        self.cli.__game__.enter_from_bar.return_value = True

        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("✓ Ficha entro exitosamente desde la barra")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1'])
    def test_handle_bear_off_black_game_over_prints_winner(self, mock_input, mock_print):
        player = MagicMock()
        player.color = 'black'
        self.cli.__game__.get_current_player.return_value = player

        self.cli.__game__.bear_off.return_value = True
        self.cli.__game__.is_game_over.return_value = True
        winner = MagicMock()
        winner.name = 'victor'
        self.cli.__game__.get_winner.return_value = winner

        result = self.cli.handle_bear_off()
        self.assertEqual(result, 'game_over')
        # winner.name is printed in uppercase in the block
        mock_print.assert_any_call(f"¡¡¡ {winner.name.upper()} HA GANADO EL JUEGO !!!")

    @patch('builtins.print')
    def test_handle_dice_roll_none_and_exception(self, mock_print):
        # None result should simply not print result line
        self.cli.__game__.roll_dice.return_value = None
        self.cli.handle_dice_roll()

        # now test generic exception path
        self.cli.__game__.roll_dice.side_effect = Exception('boom')
        self.cli.handle_dice_roll()
        mock_print.assert_any_call('Error inesperado: boom')

    @patch('builtins.print')
    def test_run_handles_generic_exception(self, mock_print):
        # patch setup_game to raise a generic exception and patch traceback.print_exc
        def raises_exc():
            raise Exception('boom')

        self.cli.setup_game = raises_exc
        import traceback
        traceback.print_exc = MagicMock()

        self.cli.run()
        self.assertFalse(self.cli.__running__)
        mock_print.assert_any_call('\nError critico: boom')

    class TestCLIMainMenuLoop(unittest.TestCase):
        def setUp(self):
            self.cli = CLI()
        # mock game to control behavior
            gm = MagicMock()
            gm.is_game_over.return_value = False
            gm.get_winner.return_value = MagicMock(name='W')
            self.cli.__game__ = gm

        # prevent screen clearing and heavy prints
            self.cli.clear_screen = MagicMock()
            self.cli.print_header = MagicMock()
            self.cli.print_board = MagicMock()
            self.cli.print_game_info = MagicMock()

        # stub handlers so they don't request extra input
            self.cli.handle_dice_roll = MagicMock()
            self.cli.handle_move_piece = MagicMock()
            self.cli.handle_enter_from_bar = MagicMock()
            self.cli.handle_bear_off = MagicMock(return_value=None)
            self.cli.handle_end_turn = MagicMock()
            self.cli.show_game_status = MagicMock()

        @patch('builtins.input')
        @patch('builtins.print')
        def test_main_menu_exercise_many_paths(self, mock_print, mock_input):
            # craft sequence of choices with ENTER confirmations after each option
            # choices: help(h), clear(c), roll(r), move(m), bar(b), bear off(s), end(e), info(i), invalid(x), quit(q->s)
            seq = []
            for ch in ['h', 'c', 'r', 'm', 'b', 's', 'e', 'i', 'x', 'q']:
                seq.append(ch)
                # most choices show a "Presiona ENTER para continuar..." -> supply blank
                if ch in ['h', 'r', 'm', 'b', 's', 'e', 'i', 'x']:
                    seq.append('')
            # add confirmation for 'q'
            seq.append('s')

            mock_input.side_effect = seq

            # run main_menu; should exit after processing the sequence
            self.cli.main_menu()

            # verify handlers were called for choices we stubbed
            self.cli.handle_dice_roll.assert_called()
            self.cli.handle_move_piece.assert_called()
            self.cli.handle_enter_from_bar.assert_called()
            self.cli.handle_end_turn.assert_called()

class TestCLIMore(unittest.TestCase):

    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.is_game_over.return_value = False
        self.mock_player = MagicMock()
        self.mock_player.name = "Jugador 1"
        self.mock_player.color = "white"

        self.mock_game.get_current_player.return_value = self.mock_player

        self.cli = CLI()
        self.cli.__game__ = self.mock_game

        # Avoid clearing screen or long prints
        self.cli.clear_screen = MagicMock()
        self.cli.print_header = MagicMock()
        self.cli.print_board = MagicMock()
        self.cli.show_available_moves = MagicMock()

    @patch('builtins.print')
    def test_display_game_state_calls_board(self, mock_print):
        mock_board = MagicMock()
        mock_board.display_board_console = MagicMock()
        self.mock_game.get_board.return_value = mock_board

        # set global pieces info
        Player.game_pieces = {'white': {'on_board': 15, 'off_board': 0}, 'black': {'on_board': 15, 'off_board': 0}}

        self.cli.display_game_state()
        mock_board.display_board_console.assert_called_once()

    @patch('builtins.print')
    def test_show_available_moves_no_values_with_bar_and_bear_off(self, mock_print):
        mock_dice = MagicMock()
        mock_dice.get_available_values.return_value = []
        self.mock_game.get_dice.return_value = mock_dice
        self.mock_game.must_enter_from_bar.return_value = True
        self.mock_game.can_bear_off.return_value = True
        self.mock_game.get_board.return_value.get_state.return_value = {'bar': {'white': 2, 'black': 0}}

        self.cli.show_available_moves()
        mock_print.assert_any_call("No hay dados disponibles - termina tu turno")
        mock_print.assert_any_call("ATENCION: Tienes 2 ficha(s) en la barra que deben entrar primero")
        mock_print.assert_any_call("Puedes comenzar a sacar fichas del tablero")

    @patch('builtins.print')
    def test_handle_dice_roll_double_prints_double(self, mock_print):
        self.mock_game.roll_dice.return_value = (4, 4)
        mock_dice = MagicMock()
        mock_dice.is_double.return_value = True
        self.mock_game.get_dice.return_value = mock_dice

        self.cli.handle_dice_roll()
        mock_print.assert_any_call("¡DOBLE! Tienes 4 movimientos disponibles")

    @patch('builtins.input', side_effect=["1", "2"])
    @patch('builtins.print')
    def test_handle_move_piece_capture_message(self, mock_print, mock_input):
        # enemy captured
        self.mock_game.move_piece.return_value = True
        board_state = {'bar': {'white': 0, 'black': 1}}
        self.mock_game.get_board.return_value.get_state.return_value = board_state
        # current player is white, so enemy_color is black with >0 in bar
        self.cli.handle_move_piece()
        mock_print.assert_any_call("¡Capturaste una ficha enemiga!")

    @patch('builtins.input', side_effect=["20"])
    @patch('builtins.print')
    def test_handle_enter_from_bar_exceptions(self, mock_print, mock_input):
        # NoPiecesInBarError
        self.mock_game.enter_from_bar.side_effect = NoPiecesInBarError("No hay fichas en la barra")
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error: No hay fichas en la barra")

        # InvalidMoveError
        self.mock_game.enter_from_bar.side_effect = InvalidMoveError("Movimiento invalido")
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Movimiento invalido: Movimiento invalido")

        # NotYourTurnError
        self.mock_game.enter_from_bar.side_effect = NotYourTurnError("No es tu turno")
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error de turno: No es tu turno")

    @patch('builtins.input', side_effect=["24"])
    @patch('builtins.print')
    def test_handle_bear_off_game_over(self, mock_print, mock_input):
        self.mock_game.bear_off.return_value = True
        self.mock_game.is_game_over.return_value = True
        winner = MagicMock()
        winner.name = "Ganador"
        self.mock_game.get_winner.return_value = winner

        result = self.cli.handle_bear_off()
        self.assertEqual(result, "game_over")
        mock_print.assert_any_call("¡¡¡ GANADOR HA GANADO EL JUEGO !!!")

    @patch('builtins.input', side_effect=["q", "s"])
    @patch('builtins.print')
    def test_main_menu_quit_confirm(self, mock_print, mock_input):
        # ensure game not over so menu shows
        self.mock_game.is_game_over.return_value = False
        # call main_menu, should exit on 'q' + 's'
        self.cli.main_menu()
        mock_print.assert_any_call("\n¡Gracias por jugar!")

    @patch('builtins.input', side_effect=["z", "q", "s"])
    @patch('builtins.print')
    def test_main_menu_invalid_option_then_quit(self, mock_print, mock_input):
        self.mock_game.is_game_over.return_value = False
        self.cli.main_menu()
        mock_print.assert_any_call("Opcion no valida. Presiona 'h' para ver la ayuda.")

    @patch('builtins.print')
    def test_print_header_and_print_dice(self, mock_print):
        # use a fresh CLI instance so we don't call the mocked print_header from setUp
        cli_real = CLI()
        cli_real.clear_screen = MagicMock()
        cli_real.__game__ = self.mock_game

        # call print_header directly to cover header lines
        cli_real.print_header()
        mock_print.assert_any_call("" + "=" * 60)

        # print_dice prints the dice representation
        self.mock_game.get_dice.return_value = (1, 2)
        cli_real.print_dice()
        mock_print.assert_any_call("Dados: (1, 2)")

    @patch('builtins.input', side_effect=["", "", ""])  # player1, player2, ENTER
    @patch('builtins.print')
    def test_setup_game_defaults(self, mock_print, mock_input):
        # Patch Game constructor used inside setup_game to return our mock_game
        with patch('cli.cli.Game', return_value=self.mock_game):
            # ensure start() is available on the mock
            self.mock_game.start = MagicMock()
            cli_real = CLI()
            cli_real.clear_screen = MagicMock()
            cli_real.setup_game()
            # after setup, __game__ should be our mock
            self.assertIs(cli_real.__game__, self.mock_game)

    @patch('builtins.print')
    def test_handle_end_turn_not_your_turn(self, mock_print):
        self.mock_game.get_dice.return_value.get_available_values.return_value = []
        self.mock_game.end_turn.side_effect = NotYourTurnError("No es tu turno")
        self.cli.handle_end_turn()
        mock_print.assert_any_call("Error: No es tu turno")

    @patch('builtins.input', side_effect=["h", "", "q", "s"])
    @patch('builtins.print')
    def test_main_menu_help_then_quit(self, mock_print, mock_input):
        # allow menu to show help then quit
        self.mock_game.is_game_over.return_value = False
        cli_real = CLI()
        cli_real.clear_screen = MagicMock()
        cli_real.print_board = MagicMock()
        cli_real.__game__ = self.mock_game
        cli_real.show_available_moves = MagicMock()
        cli_real.main_menu()
        # show_help prints help lines
        mock_print.assert_any_call("r  - Tirar dados")


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import MagicMock, patch

from cli.cli import CLI
from core.game import NotYourTurnError


class TestCLIMore(unittest.TestCase):
    def setUp(self):
        self.cli = CLI()
        # Attach a mock game to the CLI
        self.mock_game = MagicMock()
        self.cli.__game__ = self.mock_game

    @patch('builtins.print')
    def test_display_game_state_prints(self, mock_print):
        player = MagicMock()
        player.name = 'P1'
        player.color = 'white'

        dice = MagicMock()
        board = MagicMock()
        board.display_board_console = MagicMock()

        self.mock_game.get_current_player.return_value = player
        self.mock_game.get_dice.return_value = dice
        self.mock_game.get_board.return_value = board

        self.cli.display_game_state()

        # board.display_board_console should be invoked
        board.display_board_console.assert_called_once()

    @patch('builtins.print')
    def test_show_available_moves_and_warnings(self, mock_print):
        dice = MagicMock()
        dice.get_available_values.return_value = [1]
        self.mock_game.get_dice.return_value = dice
        self.mock_game.must_enter_from_bar.return_value = True
        self.mock_game.can_bear_off.return_value = True

        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 2, 'black': 0}}
        self.mock_game.get_board.return_value = board

        self.mock_game.get_current_player.return_value = MagicMock(color='white')

        self.cli.show_available_moves()

        mock_print.assert_any_call("Dados disponibles: [1]")
        mock_print.assert_any_call("ATENCION: Tienes 2 ficha(s) en la barra que deben entrar primero")
        mock_print.assert_any_call("Puedes comenzar a sacar fichas del tablero")

    @patch('builtins.print')
    def test_handle_dice_roll_success_and_double(self, mock_print):
        player = MagicMock()
        player.name = 'P1'
        player.color = 'white'
        self.mock_game.get_current_player.return_value = player

        self.mock_game.roll_dice.return_value = (2, 2)
        dice = MagicMock()
        dice.is_double.return_value = True
        self.mock_game.get_dice.return_value = dice

        self.cli.handle_dice_roll()

        mock_print.assert_any_call(f"\n{player.name} tiro: (2, 2)")
        mock_print.assert_any_call("¡DOBLE! Tienes 4 movimientos disponibles")

    @patch('builtins.print')
    def test_handle_dice_roll_not_your_turn(self, mock_print):
        self.mock_game.roll_dice.side_effect = NotYourTurnError("No es tu turno")
        self.cli.handle_dice_roll()
        mock_print.assert_any_call("Error: No es tu turno")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['a', 'b'])
    def test_handle_move_piece_invalid_input(self, mock_input, mock_print):
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Error: Las posiciones deben ser numeros")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['0', '25'])
    def test_handle_move_piece_out_of_range(self, mock_input, mock_print):
        self.cli.handle_move_piece()
        mock_print.assert_any_call("Error: Las posiciones deben estar entre 1 y 24")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', '2'])
    def test_handle_move_piece_success_capture(self, mock_input, mock_print):
        player = MagicMock()
        player.color = 'white'
        player.name = 'P1'
        self.mock_game.get_current_player.return_value = player

        # move_piece returns True
        self.mock_game.move_piece.return_value = True

        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 0, 'black': 1}}
        self.mock_game.get_board.return_value = board

        self.cli.handle_move_piece()

        mock_print.assert_any_call("✓ Movimiento realizado exitosamente")
        mock_print.assert_any_call("¡Capturaste una ficha enemiga!")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['x'])
    def test_handle_enter_from_bar_invalid_input(self, mock_input, mock_print):
        # input non-digit
        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error: La posicion debe ser un numero")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1'])
    def test_handle_enter_from_bar_out_of_range(self, mock_input, mock_print):
        # set current player white, expects 19-24
        player = MagicMock()
        player.color = 'white'
        self.mock_game.get_current_player.return_value = player

        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 1, 'black': 0}}
        self.mock_game.get_board.return_value = board

        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("Error: La posicion debe estar entre 19 y 24")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['19'])
    def test_handle_enter_from_bar_success(self, mock_input, mock_print):
        player = MagicMock()
        player.color = 'white'
        self.mock_game.get_current_player.return_value = player

        board = MagicMock()
        board.get_state.return_value = {'bar': {'white': 1, 'black': 0}}
        self.mock_game.get_board.return_value = board

        self.mock_game.enter_from_bar.return_value = True

        self.cli.handle_enter_from_bar()
        mock_print.assert_any_call("✓ Ficha entro exitosamente desde la barra")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['19'])
    def test_handle_bear_off_game_over(self, mock_input, mock_print):
        player = MagicMock()
        player.color = 'white'
        self.mock_game.get_current_player.return_value = player

        # simulate successful bear off and game over
        self.mock_game.bear_off.return_value = True
        self.mock_game.is_game_over.return_value = True
        winner = MagicMock()
        winner.name = 'Winner'
        self.mock_game.get_winner.return_value = winner

        result = self.cli.handle_bear_off()
        self.assertEqual(result, "game_over")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['n'])
    def test_handle_end_turn_abort_when_dice_available(self, mock_input, mock_print):
        dice = MagicMock()
        dice.get_available_values.return_value = [1]
        self.mock_game.get_dice.return_value = dice

        self.cli.handle_end_turn()
        # end_turn should not be called because user declined
        self.mock_game.end_turn.assert_not_called()

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['s'])
    def test_handle_end_turn_confirm(self, mock_input, mock_print):
        dice = MagicMock()
        dice.get_available_values.return_value = [1]
        self.mock_game.get_dice.return_value = dice
        self.mock_game.end_turn.return_value = True

        self.cli.handle_end_turn()
        self.mock_game.end_turn.assert_called()

    @patch('builtins.print')
    def test_show_help_and_status(self, mock_print):
        self.cli.show_help()
        mock_print.assert_any_call("r  - Tirar dados")

        # show_game_status
        state = {
            'player1': {'name': 'A', 'color': 'white', 'pieces': {'on_board': 5, 'off_board': 2}},
            'player2': {'name': 'B', 'color': 'black', 'pieces': {'on_board': 10, 'off_board': 0}}
        }
        self.mock_game.get_game_state.return_value = state
        self.cli.show_game_status()
        mock_print.assert_any_call(f"Jugador 1: {state['player1']['name']} ({state['player1']['color']})")

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
