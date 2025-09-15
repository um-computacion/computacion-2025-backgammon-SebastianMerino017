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

    def test_turns(self):
        self.assertTrue(self.p1.is_my_turn())
        self.p1.end_turn()
        self.assertTrue(self.p2.is_my_turn())
    
    def test_roll_dice_valid_turn(self):
        dice = self.p1.roll_dice()
        self.assertEqual(len(dice), 2)
        for die in dice:
            self.assertIn(die, range(1, 7))
    
    def test_roll_dice_invalid_turn(self):
        self.assertIsNone(self.p2.roll_dice())