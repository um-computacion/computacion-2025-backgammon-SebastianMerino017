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
        board.pos = [None for _ in range(24)]
        board.pos[0] = ["white", 3]
        board.pos[1] = ["white", 8]
    
        board_draw = board.draw()
    
        self.assertEqual(len(board_draw), 12)
    
        self.assertEqual(board_draw[11][0], 'W')
        self.assertEqual(board_draw[11][1], 'W')
        self.assertEqual(board_draw[11][2], 'W')

    def test_draw_more_than_five_pieces(self):
        board = Board()
        board.pos = [None for _ in range(24)]
        board.pos[5] = ["white", 7]
        
        board_draw = board.draw()
        
        self.assertEqual(board_draw[6][0], 'W')
        self.assertEqual(board_draw[6][1], 'W')
        self.assertEqual(board_draw[6][2], 'W')
        self.assertEqual(board_draw[6][3], 'W')
        self.assertEqual(board_draw[6][4], '3')

    def test_get_piece_white(self):
        self.board.pos[0] = ["white", 2]
        self.assertEqual(self.board.get_piece(0), 'W')
    
    def test_get_piece_black(self):
        self.board.pos[5] = ["black", 3]
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