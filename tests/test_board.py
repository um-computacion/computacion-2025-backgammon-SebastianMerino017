import unittest
from core.board import Board
from unittest.mock import patch

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = Board()
    
    def test_initial_setup(self):
        board = Board()
        
        self.assertEqual(board.__pos__[0], ["white", 2])
        self.assertEqual(board.__pos__[11], ["white", 5])
        self.assertEqual(board.__pos__[16], ["white", 3])
        self.assertEqual(board.__pos__[18], ["white", 5])
        
        self.assertEqual(board.__pos__[23], ["black", 2])
        self.assertEqual(board.__pos__[12], ["black", 5])
        self.assertEqual(board.__pos__[7], ["black", 3])
        self.assertEqual(board.__pos__[5], ["black", 5])
        
        self.assertEqual(board.__bar__, {"white": 0, "black": 0})
        self.assertEqual(board.__off_board__, {"white": 0, "black": 0})
    
    def test_draw(self):
        board = Board()
        board.__pos__ = [None for _ in range(24)]
        board.__pos__[0] = ["white", 3]
        board.__pos__[1] = ["white", 8]
        
        board_draw = board.draw()
        
        self.assertEqual(len(board_draw), 12)
        
        self.assertEqual(board_draw[11][0], 'W')
        self.assertEqual(board_draw[11][1], 'W')
        self.assertEqual(board_draw[11][2], 'W')
    
    def test_draw_more_than_five_pieces(self):
        board = Board()
        board.__pos__ = [None for _ in range(24)]
        board.__pos__[10] = ["white", 7]
        
        board_draw = board.draw()
        
        self.assertEqual(board_draw[1][0], 'W')
        self.assertEqual(board_draw[1][1], 'W')
        self.assertEqual(board_draw[1][2], 'W')
        self.assertEqual(board_draw[1][3], 'W')
        self.assertEqual(board_draw[1][4], '3')
    
    def test_get_piece_white(self):
        self.board.__pos__[0] = ["white", 2]
        self.assertEqual(self.board.get_piece(0), 'W')
    
    def test_get_piece_black(self):
        self.board.__pos__[5] = ["black", 3]
        self.assertEqual(self.board.get_piece(5), 'B')
    
    def test_is_valid_position_valid(self):
        self.assertTrue(self.board.is_valid_position(0))
        self.assertTrue(self.board.is_valid_position(12))
        self.assertTrue(self.board.is_valid_position(23))
    
    def test_is_valid_position_invalid(self):
        self.assertFalse(self.board.is_valid_position(-1))
        self.assertFalse(self.board.is_valid_position(24))
        self.assertFalse(self.board.is_valid_position(100))
        self.assertFalse(self.board.is_valid_position("0"))
    
    def test_get_position_info_valid(self):
        info = self.board.get_position_info(0)
        self.assertEqual(info, ["white", 2])
    
    def test_get_position_info_invalid(self):
        info = self.board.get_position_info(25)
        self.assertIsNone(info)
    
    def test_get_position_info_empty(self):
        self.board.__pos__[10] = None
        info = self.board.get_position_info(10)
        self.assertIsNone(info)
    
    def test_can_place_piece_empty_position(self):
        self.board.__pos__[10] = None
        self.assertTrue(self.board.can_place_piece(10, "white"))
    
    def test_can_place_piece_same_color(self):
        self.board.__pos__[0] = ["white", 2]
        self.assertTrue(self.board.can_place_piece(0, "white"))
    
    def test_can_place_piece_one_enemy(self):
        self.board.__pos__[10] = ["black", 1]
        self.assertTrue(self.board.can_place_piece(10, "white"))
    
    def test_can_place_piece_blocked(self):
        self.board.__pos__[10] = ["black", 2]
        self.assertFalse(self.board.can_place_piece(10, "white"))
    
    def test_can_place_piece_invalid_position(self):
        self.assertFalse(self.board.can_place_piece(25, "white"))
    
    def test_move_piece_simple(self):
        self.board.__pos__[0] = ["white", 2]
        self.board.__pos__[3] = None
        
        result = self.board.move_piece(0, 3, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__pos__[0], ["white", 1])
        self.assertEqual(self.board.__pos__[3], ["white", 1])
    
    def test_move_piece_to_same_color(self):
        self.board.__pos__[0] = ["white", 2]
        self.board.__pos__[3] = ["white", 1]
        
        result = self.board.move_piece(0, 3, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__pos__[0], ["white", 1])
        self.assertEqual(self.board.__pos__[3], ["white", 2])
    
    def test_move_piece_capture(self):
        self.board.__pos__[0] = ["white", 2]
        self.board.__pos__[3] = ["black", 1]
        
        result = self.board.move_piece(0, 3, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__pos__[0], ["white", 1])
        self.assertEqual(self.board.__pos__[3], ["white", 1])
        self.assertEqual(self.board.__bar__["black"], 1)
    
    def test_move_piece_invalid_from(self):
        result = self.board.move_piece(25, 3, "white")
        self.assertFalse(result)
    
    def test_move_piece_invalid_to(self):
        result = self.board.move_piece(0, 25, "white")
        self.assertFalse(result)
    
    def test_move_piece_empty_origin(self):
        self.board.__pos__[10] = None
        result = self.board.move_piece(10, 13, "white")
        self.assertFalse(result)
    
    def test_move_piece_wrong_color(self):
        self.board.__pos__[0] = ["white", 2]
        result = self.board.move_piece(0, 3, "black")
        self.assertFalse(result)
    
    def test_move_piece_blocked(self):
        self.board.__pos__[0] = ["white", 2]
        self.board.__pos__[3] = ["black", 2]
        
        result = self.board.move_piece(0, 3, "white")
        self.assertFalse(result)
    
    def test_bear_off_white_valid(self):
        self.board.__pos__[20] = ["white", 2]
        initial_off_board = self.board.__off_board__["white"]
        
        result = self.board.bear_off(20, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__pos__[20], ["white", 1])
        self.assertEqual(self.board.__off_board__["white"], initial_off_board + 1)
    
    def test_bear_off_black_valid(self):
        self.board.__pos__[3] = ["black", 2]
        initial_off_board = self.board.__off_board__["black"]
        
        result = self.board.bear_off(3, "black")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__pos__[3], ["black", 1])
        self.assertEqual(self.board.__off_board__["black"], initial_off_board + 1)
    
    def test_bear_off_last_piece(self):
        self.board.__pos__[20] = ["white", 1]
        
        result = self.board.bear_off(20, "white")
        
        self.assertTrue(result)
        self.assertIsNone(self.board.__pos__[20])
        self.assertEqual(self.board.__off_board__["white"], 1)
    
    def test_bear_off_wrong_position_white(self):
        self.board.__pos__[10] = ["white", 2]
        result = self.board.bear_off(10, "white")
        self.assertFalse(result)
    
    def test_bear_off_wrong_position_black(self):
        self.board.__pos__[10] = ["black", 2]
        result = self.board.bear_off(10, "black")
        self.assertFalse(result)
    
    def test_bear_off_invalid_position(self):
        result = self.board.bear_off(25, "white")
        self.assertFalse(result)
    
    def test_bear_off_empty_position(self):
        self.board.__pos__[20] = None
        result = self.board.bear_off(20, "white")
        self.assertFalse(result)
    
    def test_bear_off_wrong_color(self):
        self.board.__pos__[20] = ["black", 2]
        result = self.board.bear_off(20, "white")
        self.assertFalse(result)
    
    def test_enter_from_bar_white_valid(self):
        self.board.__bar__["white"] = 1
        self.board.__pos__[20] = None
        
        result = self.board.enter_from_bar(20, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__bar__["white"], 0)
        self.assertEqual(self.board.__pos__[20], ["white", 1])
    
    def test_enter_from_bar_black_valid(self):
        self.board.__bar__["black"] = 1
        self.board.__pos__[3] = None
        
        result = self.board.enter_from_bar(3, "black")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__bar__["black"], 0)
        self.assertEqual(self.board.__pos__[3], ["black", 1])
    
    def test_enter_from_bar_with_capture(self):
        self.board.__bar__["white"] = 1
        self.board.__pos__[20] = ["black", 1]
        
        result = self.board.enter_from_bar(20, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__bar__["white"], 0)
        self.assertEqual(self.board.__bar__["black"], 1)
        self.assertEqual(self.board.__pos__[20], ["white", 1])
        self.assertEqual(self.board.__bar__["white"], 0)

        self.assertEqual(self.board.pos[20], ["white", 1])
    
    def test_enter_from_bar_black_valid(self):
        self.board.__bar__["black"] = 1
        self.board.__pos__[3] = None
        
        result = self.board.enter_from_bar(3, "black")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__bar__["black"], 0)
        self.assertEqual(self.board.__pos__[3], ["black", 1])
    
    def test_enter_from_bar_with_capture(self):
        self.board.__bar__["white"] = 1
        self.board.__pos__[20] = ["black", 1]
        
        result = self.board.enter_from_bar(20, "white")
        
        self.assertTrue(result)
        self.assertEqual(self.board.__bar__["white"], 0)
        self.assertEqual(self.board.__bar__["black"], 1)
        self.assertEqual(self.board.__pos__[20], ["white", 1])
    
    def test_enter_from_bar_no_pieces_in_bar(self):
        self.board.__bar__["white"] = 0
        result = self.board.enter_from_bar(20, "white")
        self.assertFalse(result)
    
    def test_enter_from_bar_wrong_zone_white(self):
        self.board.__bar__["white"] = 1
        result = self.board.enter_from_bar(10, "white")
        self.assertFalse(result)
    
    def test_enter_from_bar_wrong_zone_black(self):
        self.board.__bar__["black"] = 1
        result = self.board.enter_from_bar(10, "black")
        self.assertFalse(result)
    
    def test_enter_from_bar_blocked(self):
        self.board.__bar__["white"] = 1
        self.board.__pos__[20] = ["black", 2]
        
        result = self.board.enter_from_bar(20, "white")
        self.assertFalse(result)
    
    def test_count_pieces_initial(self):
        white_count = self.board.count_pieces("white")
        black_count = self.board.count_pieces("black")
        
        self.assertEqual(white_count, 15)
        self.assertEqual(black_count, 15)
    
    def test_count_pieces_with_bar(self):
        self.board.__bar__["white"] = 2
        white_count = self.board.count_pieces("white")
        
    
    def test_count_pieces_after_bear_off(self):
        self.board.__pos__[20] = ["white", 1]
        self.board.bear_off(20, "white")
        
        white_count = self.board.count_pieces("white")
        
    
    def test_get_state(self):
        state = self.board.get_state()
        
        self.assertIn("positions", state)
        self.assertIn("bar", state)
        self.assertIn("off_board", state)
        self.assertEqual(len(state["positions"]), 24)
    
    def test_get_state_is_copy(self):
        state = self.board.get_state()
        state["bar"]["white"] = 100
        
        self.assertEqual(self.board.__bar__["white"], 0)
    
    def test_reset_board(self):
        self.board.__pos__[0] = ["white", 10]
        self.board.__bar__["white"] = 5
        self.board.__off_board__["black"] = 3
        
        self.board.reset_board()
        
        self.assertEqual(self.board.__pos__[0], ["white", 2])
        self.assertEqual(self.board.__bar__["white"], 0)
        self.assertEqual(self.board.__off_board__["black"], 0)

    def setUp(self):
        self.board = Board()

    def test_is_valid_position_and_get_position_info(self):
        self.assertTrue(self.board.is_valid_position(0))
        self.assertTrue(self.board.is_valid_position(23))
        self.assertFalse(self.board.is_valid_position(24))
        self.assertIsNone(self.board.get_position_info(24))

    def test_can_place_piece_various(self):
        self.assertTrue(self.board.can_place_piece(1, 'white'))

        self.board.__pos__[1] = ['white', 2]
        self.assertTrue(self.board.can_place_piece(1, 'white'))

        self.board.__pos__[2] = ['black', 1]
        self.assertTrue(self.board.can_place_piece(2, 'white'))

        self.board.__pos__[3] = ['black', 2]
        self.assertFalse(self.board.can_place_piece(3, 'white'))

    def test_move_piece_invalid_cases(self):
        self.assertFalse(self.board.move_piece('white', -1, 5))
        self.board.__pos__[4] = None
        self.assertFalse(self.board.move_piece('white', 4, 5))

    def test_move_piece_capture_and_remove_from(self):
        self.board.__pos__[0] = ['white', 1]
        self.board.__pos__[1] = ['black', 1]
        before_bar_black = self.board.__bar__['black']

        ok = self.board.move_piece('white', 0, 1)
        self.assertTrue(ok)
        self.assertEqual(self.board.__bar__['black'], before_bar_black + 1)
        self.assertEqual(self.board.__pos__[1][0], 'white')

    def test_move_piece_increment_on_target(self):
        self.board.__pos__[6] = ['white', 2]
        self.board.__pos__[7] = ['white', 3]
        ok = self.board.move_piece('white', 6, 7)
        self.assertTrue(ok)
        self.assertEqual(self.board.__pos__[7][1], 4)

    def test_bear_off_wrong_and_success(self):
        self.board.__pos__[0] = ['black', 1]
        self.assertFalse(self.board.bear_off(0, 'white'))

        self.board.__pos__[10] = ['white', 1]
        self.assertFalse(self.board.bear_off(10, 'white'))

        self.board.__pos__[23] = ['white', 1]
        before = self.board.__off_board__['white']
        ok = self.board.bear_off(23, 'white')
        self.assertTrue(ok)
        self.assertEqual(self.board.__off_board__['white'], before + 1)

    def test_enter_from_bar_cases(self):
        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.enter_from_bar(19, 'white'))

        self.board.__bar__['white'] = 1
        self.board.__pos__[19] = ['black', 2]
        self.assertFalse(self.board.enter_from_bar(19, 'white'))

        self.board.__pos__[10] = None
        self.assertFalse(self.board.enter_from_bar(10, 'white'))

        self.board.__pos__[18] = ['black', 1]
        self.board.__bar__['white'] = 1
        before_black_bar = self.board.__bar__['black']
        ok = self.board.enter_from_bar(18, 'white')
        self.assertTrue(ok)
        self.assertEqual(self.board.__bar__['black'], before_black_bar + 1)

    def test_count_and_has_pieces_in_home_board(self):
        self.board.reset_board()
        self.board.__bar__['white'] = 2
        c = self.board.count_pieces('white')
        self.assertTrue(c >= 2)

        self.board.__pos__[0] = ['white', 1]
        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.has_pieces_in_home_board('white'))

        self.board.reset_board()
        for i in range(18):
            self.board.__pos__[i] = None
        self.board.__bar__['white'] = 0
        self.assertTrue(self.board.has_pieces_in_home_board('white'))

    def test_get_state_is_copy_and_reset_board(self):
        st = self.board.get_state()
        st['positions'][0] = None
        st2 = self.board.get_state()
        self.assertIsNotNone(st2['positions'][0])

        self.board.__pos__[0] = None
        self.board.reset_board()
        self.assertIsNotNone(self.board.__pos__[0])

    def test_is_target_valid_and_reentry(self):
        self.assertFalse(self.board.is_target_valid(30, 'white'))

        self.board.__pos__[4] = ['black', 3]
        self.assertFalse(self.board.is_target_valid(4, 'white'))

        self.board.__pos__[5] = None
        self.assertTrue(self.board.is_target_valid(5, 'white'))
        self.assertTrue(self.board.is_re_entry_target_valid(5, 'white'))

    def test_is_valid_move_various(self):
        self.assertFalse(self.board.is_valid_move('white', 0, 'x'))

        self.board.__bar__['white'] = 0
        self.assertFalse(self.board.is_valid_move('white', 'bar', 19))

        self.board.__bar__['white'] = 1
        self.assertFalse(self.board.is_valid_move('white', 'bar', 5))

        self.assertFalse(self.board.is_valid_move('white', 'a', 5))

        self.board.__pos__[2] = None
        self.assertFalse(self.board.is_valid_move('white', 2, 5))

        self.board.__pos__[10] = ['white', 1]
        self.assertFalse(self.board.is_valid_move('white', 10, 9))

        self.board.__pos__[10] = ['white', 1]
        self.board.__pos__[13] = None
        self.assertTrue(self.board.is_valid_move('white', 10, 13))

class TestBoardMore(unittest.TestCase):
    def test_draw_with_many_pieces(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[0] = ['white', 7]
        board_draw = b.draw()
        self.assertEqual(len(board_draw), 12)
        self.assertEqual(len(board_draw[0]), 5)
        found_non_space = any(cell != ' ' for row in board_draw for cell in row)
        self.assertTrue(found_non_space)

    def test_draw_full_board_various(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[12] = ['black', 6]
        b._Board__pos__[11] = ['white', 2]
        res = b.draw_full_board()
        self.assertIn('upper', res)
        self.assertIn('lower', res)

    def test_display_board_console_runs(self):
        b = Board()
        with patch('builtins.print') as mock_print:
            b.display_board_console()
            self.assertTrue(mock_print.called)

    def test_move_piece_stack_increment(self):
        b = Board()
        res = b.move_piece(11, 16, 'white')
        self.assertTrue(res)
        state = b.get_state()['positions']
        self.assertEqual(state[11][1], 4)
        self.assertEqual(state[16][1], 4)

    def test_enter_from_bar_blocked_and_invalid_zone(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[18] = ['black', 2]
        b._Board__bar__ = {'white': 1, 'black': 0}
        res = b.enter_from_bar(18, 'white')
        self.assertFalse(res)

        b._Board__bar__ = {'white': 1, 'black': 0}
        res2 = b.enter_from_bar(0, 'white')
        self.assertFalse(res2)

    def test_is_target_valid_out_of_range(self):
        b = Board()
        self.assertFalse(b.is_target_valid(-1, 'white'))
        self.assertFalse(b.is_target_valid(24, 'black'))

    def test_is_target_valid_enemy_block(self):
        b = Board()
        self.assertFalse(b.is_target_valid(5, 'white'))

    def test_draw_full_board_numeric_overflow(self):
        b = Board()
        self.assertIsNotNone(b.draw_full_board())

    def test_has_pieces_in_home_board_black_and_bar(self):
        b = Board()
        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[10] = ['black', 1]
        self.assertFalse(b.has_pieces_in_home_board('black'))

        b._Board__pos__ = [None for _ in range(24)]
        b._Board__pos__[0] = ['black', 15]
        b._Board__bar__ = {'white': 0, 'black': 1}
        self.assertFalse(b.has_pieces_in_home_board('black'))




if __name__ == '__main__':
    unittest.main(verbosity=2)