import unittest
from core.board import Board


class TestBoardAdditional(unittest.TestCase):

    """Additional Board tests to increase coverage.

    Exercises branches in core.board.Board methods.
    """

    def setUp(self):
        self.board = Board()

    def test_is_valid_position_and_get_position_info(self):
        self.assertTrue(self.board.is_valid_position(0))
        self.assertTrue(self.board.is_valid_position(23))
        self.assertFalse(self.board.is_valid_position(24))
        self.assertIsNone(self.board.get_position_info(24))

    def test_can_place_piece_various(self):
        # empty position
        self.assertTrue(self.board.can_place_piece(1, 'white'))

        # same color stacked
        self.board.__pos__[1] = ['white', 2]
        self.assertTrue(self.board.can_place_piece(1, 'white'))

        # enemy single - can place
        self.board.__pos__[2] = ['black', 1]
        self.assertTrue(self.board.can_place_piece(2, 'white'))

        # enemy multiple - cannot place
        self.board.__pos__[3] = ['black', 2]
        self.assertFalse(self.board.can_place_piece(3, 'white'))

    def test_move_piece_invalid_cases(self):
        # invalid positions
        self.assertFalse(self.board.move_piece('white', -1, 5))
        # nothing at from_pos
        self.board.__pos__[4] = None
        self.assertFalse(self.board.move_piece('white', 4, 5))

    def test_move_piece_capture_and_remove_from(self):
        # set from_pos with one white piece
        self.board.__pos__[0] = ['white', 1]
        # set to_pos with single black piece to capture
        self.board.__pos__[1] = ['black', 1]
        before_bar_black = self.board.__bar__['black']

        ok = self.board.move_piece('white', 0, 1)
        self.assertTrue(ok)
        # after capture, black bar incremented
        self.assertEqual(self.board.__bar__['black'], before_bar_black + 1)
        # to_pos now has white piece
        self.assertEqual(self.board.__pos__[1][0], 'white')

    def test_move_piece_increment_on_target(self):
        # from_pos has 2 pieces
        self.board.__pos__[6] = ['white', 2]
        # to_pos has same color
        self.board.__pos__[7] = ['white', 3]
        ok = self.board.move_piece('white', 6, 7)
        self.assertTrue(ok)
        self.assertEqual(self.board.__pos__[7][1], 4)

    def test_bear_off_wrong_and_success(self):
        # wrong color on pos
        self.board.__pos__[0] = ['black', 1]
        self.assertFalse(self.board.bear_off(0, 'white'))

        # white cannot bear off from non-home
        self.board.__pos__[10] = ['white', 1]
        self.assertFalse(self.board.bear_off(10, 'white'))

        # successful bear off
        self.board.__pos__[23] = ['white', 1]
        before = self.board.__off_board__['white']
        ok = self.board.bear_off(23, 'white')
        self.assertTrue(ok)
        self.assertEqual(self.board.__off_board__['white'], before + 1)

    def test_enter_from_bar_cases(self):
        # no pieces in bar
        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.enter_from_bar(19, 'white'))

        # set bar and blocked target (enemy multiple)
        self.board.__bar__['white'] = 1
        self.board.__pos__[19] = ['black', 2]
        self.assertFalse(self.board.enter_from_bar(19, 'white'))

        # wrong zone for white
        self.board.__pos__[10] = None
        self.assertFalse(self.board.enter_from_bar(10, 'white'))

        # capture on enter
        self.board.__pos__[18] = ['black', 1]
        self.board.__bar__['white'] = 1
        before_black_bar = self.board.__bar__['black']
        ok = self.board.enter_from_bar(18, 'white')
        self.assertTrue(ok)
        self.assertEqual(self.board.__bar__['black'], before_black_bar + 1)

    def test_count_and_has_pieces_in_home_board(self):
        # set few positions and bars
        self.board.reset_board()
        # count should include on board and bar
        self.board.__bar__['white'] = 2
        c = self.board.count_pieces('white')
        self.assertTrue(c >= 2)

        # has_pieces_in_home_board false if pieces outside home
        self.board.__pos__[0] = ['white', 1]
        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.has_pieces_in_home_board('white'))

        # only home pieces
        self.board.reset_board()
        # remove any white outside home
        for i in range(18):
            self.board.__pos__[i] = None
        self.board.__bar__['white'] = 0
        self.assertTrue(self.board.has_pieces_in_home_board('white'))

    def test_get_state_is_copy_and_reset_board(self):
        st = self.board.get_state()
        # mutate returned state should not affect internal
        st['positions'][0] = None
        st2 = self.board.get_state()
        self.assertIsNotNone(st2['positions'][0])

        # test reset_board sets initial positions
        self.board.__pos__[0] = None
        self.board.reset_board()
        self.assertIsNotNone(self.board.__pos__[0])

    def test_is_target_valid_and_reentry(self):
        # out of range
        self.assertFalse(self.board.is_target_valid(30, 'white'))

        # place enemy multiple
        self.board.__pos__[4] = ['black', 3]
        self.assertFalse(self.board.is_target_valid(4, 'white'))

        # empty target valid
        self.board.__pos__[5] = None
        self.assertTrue(self.board.is_target_valid(5, 'white'))
        self.assertTrue(self.board.is_re_entry_target_valid(5, 'white'))

    def test_is_valid_move_various(self):
        # to_point invalid type
        self.assertFalse(self.board.is_valid_move('white', 0, 'x'))

        # from bar but no pieces
        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.is_valid_move('white', 'bar', 19))

        # from bar with pieces but wrong zone
        self.board.__bar__['white'] = 1
        self.assertFalse(self.board.is_valid_move('white', 'bar', 5))

        # normal from/to invalid types
        self.assertFalse(self.board.is_valid_move('white', 'a', 5))

        # no piece at from
        self.board.__pos__[2] = None
        self.assertFalse(self.board.is_valid_move('white', 2, 5))

        # set piece and test direction invalid
        self.board.__pos__[10] = ['white', 1]
        self.assertFalse(self.board.is_valid_move('white', 10, 9))

        # valid move
        self.board.__pos__[10] = ['white', 1]
        # ensure target valid
        self.board.__pos__[13] = None
        self.assertTrue(self.board.is_valid_move('white', 10, 13))


if __name__ == '__main__':
    unittest.main()
