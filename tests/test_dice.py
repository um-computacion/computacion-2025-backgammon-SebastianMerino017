from core.dice import get_dice
from unittest import TestCase
from unittest.mock import patch

class TestDice(TestCase):
    @patch('random.randint', side_effect=[5, 2])
    def test_simple(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 5)
        self.assertEqual(dice[1], 2)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', return_value=1)
    def test_complex(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 1)
        self.assertEqual(dice[1], 1)
        self.assertEqual(dice[2], 1)
        self.assertEqual(dice[3], 1)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=Exception("error!!"))
    def test_error(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 0)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 1)

    def test_double(self):
        with patch('random.randint', side_effect=[5, 2]) as randint_patched:
            dice = get_dice()
            self.assertEqual(len(dice), 2)
            self.assertEqual(dice[0], 5)
            self.assertEqual(dice[1], 2)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=[6, 6])
    def test_max_values(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 6)
        self.assertEqual(dice[1], 6)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=[1, 1])
    def test_min_values(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 1)
        self.assertEqual(dice[1], 1)
        self.assertEqual(dice[2], 1)
        self.assertEqual(dice[3], 1)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=[3, 4])
    def test_normal_values(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 3)
        self.assertEqual(dice[1], 4)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    def test_multiple_calls(self):
        with patch('random.randint', side_effect=[2, 3, 5, 1]) as randint_patched:
            dice1 = get_dice()
            dice2 = get_dice()
            self.assertEqual(len(dice1), 2)
            self.assertEqual(len(dice2), 2)
            self.assertEqual(dice1[0], 2)
            self.assertEqual(dice1[1], 3)
            self.assertEqual(dice2[0], 5)
            self.assertEqual(dice2[1], 1)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 4)

    @patch('random.randint', side_effect=[1, 6])
    def test_mixed_extremes(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 2)
        self.assertEqual(dice[0], 1)
        self.assertEqual(dice[1], 6)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)


    @patch('random.randint', side_effect=[4, 4])
    def test_equal_middle_values(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 4)
        self.assertEqual(dice[0], 4)
        self.assertEqual(dice[1], 4)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 2)

    @patch('random.randint', side_effect=[Exception("network error"), 3])
    def test_partial_error(self, randint_patched):
        dice = get_dice()
        self.assertEqual(len(dice), 0)
        self.assertTrue(randint_patched.called)
        self.assertEqual(randint_patched.call_count, 1)

    def test_context_manager_multiple(self):
        with patch('random.randint', side_effect=[6, 1, 2, 5, 4, 3]) as randint_patched:
            dice1 = get_dice()
            dice2 = get_dice()
            dice3 = get_dice()
            self.assertEqual(len(dice1), 2)
            self.assertEqual(len(dice2), 2)
            self.assertEqual(len(dice3), 2)
            self.assertEqual(dice1[0], 6)
            self.assertEqual(dice1[1], 1)
            self.assertEqual(dice2[0], 2)
            self.assertEqual(dice2[1], 5)
            self.assertEqual(dice3[0], 4)
            self.assertEqual(dice3[1], 3)
            self.assertTrue(randint_patched.called)
            self.assertEqual(randint_patched.call_count, 6)