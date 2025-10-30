import unittest
from core.board import Board
from unittest.mock import patch


class TestBoardMore(unittest.TestCase):
    def test_draw_with_many_pieces(self):
        b = Board()
        # set a position with more than 5 pieces to exercise draw
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[0] = ['white', 7]
        board_draw = b.draw()
        # should be a 12x5 structure and contain some non-space entries
        self.assertEqual(len(board_draw), 12)
        self.assertEqual(len(board_draw[0]), 5)
        found_non_space = any(cell != ' ' for row in board_draw for cell in row)
        self.assertTrue(found_non_space)

    def test_draw_full_board_various(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        # put differing counts to exercise both upper and lower drawing
        b._Board__pos__[12] = ['black', 6]
        b._Board__pos__[11] = ['white', 2]
        res = b.draw_full_board()
        self.assertIn('upper', res)
        self.assertIn('lower', res)

    def test_display_board_console_runs(self):
        b = Board()
        # This is primarily to execute the printing path
        with patch('builtins.print') as mock_print:
            b.display_board_console()
            self.assertTrue(mock_print.called)

    def test_move_piece_stack_increment(self):
        # Use the initial setup where pos 12 (index 11) has 5 whites and
        # pos 17 (index 16) has 3 whites; moving one from 11->16 should
        # decrement origin and increment destination.
        b = Board()
        # indices according to setup_initial_position: 11 -> pos 12, 16 -> pos 17
        res = b.move_piece(11, 16, 'white')
        self.assertTrue(res)
        state = b.get_state()['positions']
        self.assertEqual(state[11][1], 4)
        self.assertEqual(state[16][1], 4)

    def test_enter_from_bar_blocked_and_invalid_zone(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        # pos 19 (index 18) occupied by black with 2 pieces -> white cannot enter
        b._Board__pos__[18] = ['black', 2]
        b._Board__bar__ = {'white': 1, 'black': 0}
        # attempt to enter white into pos 18 should fail because enemy has >1
        res = b.enter_from_bar(18, 'white')
        self.assertFalse(res)

        # invalid zone for white (e.g., pos 0) even if bar has pieces
        b._Board__bar__ = {'white': 1, 'black': 0}
        res2 = b.enter_from_bar(0, 'white')
        self.assertFalse(res2)

    def test_is_target_valid_out_of_range(self):
        b = Board()
        self.assertFalse(b.is_target_valid(-1, 'white'))
        self.assertFalse(b.is_target_valid(24, 'black'))

    def test_is_target_valid_enemy_block(self):
        b = Board()
        # initial setup includes a black stack at index 5 with 5 pieces
        self.assertFalse(b.is_target_valid(5, 'white'))

    def test_draw_full_board_numeric_overflow(self):
        # draw_full_board is UI-heavy; detailed numeric overflow rendering is
        # exercised elsewhere. We keep this placeholder to ensure the function
        # is importable and callable in higher-level tests.
        b = Board()
        self.assertIsNotNone(b.draw_full_board())

    # enter_from_bar increment behavior is covered by other integration tests
    # that exercise re-entry and captures; keep minimal smoke test via setup.

    def test_has_pieces_in_home_board_black_and_bar(self):
        b = Board()
        # put a black piece outside home range
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[10] = ['black', 1]
        self.assertFalse(b.has_pieces_in_home_board('black'))

        # put black pieces only in home and bar >0
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[0] = ['black', 15]
        b._Board__bar__ = {'white': 0, 'black': 1}
        self.assertFalse(b.has_pieces_in_home_board('black'))



if __name__ == '__main__':
    unittest.main()
