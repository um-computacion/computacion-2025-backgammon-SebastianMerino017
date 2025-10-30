import unittest
from unittest.mock import patch
from core.dice import Dice, get_dice


class TestDiceClass(unittest.TestCase):
    def test_roll_and_values(self):
        with patch('core.dice.get_dice', return_value=(3, 4)):
            d = Dice()
            res = d.roll()
            self.assertEqual(res, (3, 4))
            self.assertEqual(d.get_values(), [3, 4])
            self.assertFalse(d.is_double())
            self.assertTrue(d.has_available_values())

    def test_double_roll_and_use(self):
        with patch('core.dice.get_dice', return_value=(2, 2, 2, 2)):
            d = Dice()
            res = d.roll()
            self.assertEqual(res, (2, 2))
            self.assertTrue(d.is_double())
            vals = d.get_available_values()
            self.assertEqual(vals.count(2), 4)
            self.assertTrue(d.use_value(2))
            self.assertTrue(len(d.get_available_values()) < 4)

    def test_use_value_invalid(self):
        d = Dice()
        self.assertFalse(d.use_value(3))

    def test_str_variants(self):
        d = Dice()
        self.assertIn('Dados sin tirar', str(d))
        with patch('core.dice.get_dice', return_value=(5, 6)):
            d.roll()
            s = str(d)
            self.assertIn('Tirada:', s)


if __name__ == '__main__':
    unittest.main()
