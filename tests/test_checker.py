import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):
    def test_init(self):
        checker = Checker("black")
        self.assertEqual(checker.get_color(), "black")
        self.assertEqual(checker.get_position(), None)
        self.assertFalse(checker.is_captured())

if __name__ == '__main__':
    unittest.main()