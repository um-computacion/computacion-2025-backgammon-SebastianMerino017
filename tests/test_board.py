import unittest
from core.board import Board

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


if __name__ == '__main__':
    unittest.main(verbosity=2)



