import unittest
from unittest.mock import patch
from core.player import Player

class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        Player.reset_game()
        self.p1 = Player("Juan", "white")
        self.p2 = Player("María", "black")
    
    def tearDown(self):
        Player.reset_game()
    
    def test_initial_state(self):
        self.assertEqual(self.p1.name, "Juan")
        self.assertEqual(self.p1.color, "white")
        self.assertEqual(Player.current_turn, "white")
        self.assertEqual(Player.game_pieces['white']['on_board'], 15)