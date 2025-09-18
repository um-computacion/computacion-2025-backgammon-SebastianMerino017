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

    from unittest.mock import patch

    def test_play_dice_valid_turn(self):
        with patch("random.randint", side_effect=[1, 2]):
            dice = self.p1.roll_dice()
        self.p1.play_dice(dice)
        self.assertEqual(self.p1.dice, [1, 2])
        self.assertEqual(self.p1.dice[0], 1)
        self.assertEqual(self.p1.dice[1], 2)

    def test_play_dice_invalid_turn(self):
        with patch("random.randint", side_effect=[1, 2]):
            dice = self.p1.roll_dice()
        self.p2.play_dice(dice)
        self.assertEqual(self.p2.dice, [1, 2])
        self.assertEqual(self.p2.dice[0], 1)
        self.assertEqual(self.p2.dice[1], 2)

