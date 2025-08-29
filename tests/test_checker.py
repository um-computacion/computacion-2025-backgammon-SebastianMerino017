import unittest
import unittest
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from core.checker import Checker

class TestChecker(unittest.TestCase):
    def test_init(self):
        checker = Checker("black")
        self.assertEqual(checker.get_color(), "black")
        self.assertEqual(checker.get_position(), None)
        self.assertFalse(checker.is_captured())

    def test_init_with_position(self):
        checker = Checker("white", 5)
        self.assertEqual(checker.get_color(), "white")
        self.assertEqual(checker.get_position(), 5)
        self.assertFalse(checker.is_captured())

    def test_set_position(self):
        checker = Checker("red")
        checker.set_position(10)
        self.assertEqual(checker.get_position(), 10)



if __name__ == '__main__':
    unittest.main()