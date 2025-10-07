import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
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