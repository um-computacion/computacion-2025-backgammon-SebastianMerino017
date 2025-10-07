import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
    def test_draw(self):
        board = Board()
        board.pos[0] = ('white', 3)
        board.pos[1] = ('white', 8)
        board.pos[23] = ('black', 1)
        board.pos[22] = ('black', 3)
        print(board.draw())
        board_draw = board.draw()
        print(f"board 0, 11: {board_draw[11][0]}")