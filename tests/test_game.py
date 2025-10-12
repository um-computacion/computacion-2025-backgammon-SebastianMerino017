import unittest
from unittest.mock import patch, MagicMock
from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.player import Player


class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game("Juan", "María")
    
    def tearDown(self):
        Player.reset_game()
    
    def test_initialization(self):
        self.assertIsNotNone(self.game.__board__)
        self.assertIsNotNone(self.game.__player1__)
        self.assertIsNotNone(self.game.__player2__)
        self.assertIsNotNone(self.game.__dice__)
        self.assertEqual(self.game.__player1__.name, "Juan")
        self.assertEqual(self.game.__player2__.name, "María")
        self.assertEqual(self.game.__player1__.color, "white")
        self.assertEqual(self.game.__player2__.color, "black")
        self.assertIsNone(self.game.__winner__)
        self.assertFalse(self.game.__game_started__)
    
    def test_start_game(self):
        result = self.game.start()
        self.assertTrue(result)
        self.assertTrue(self.game.__game_started__)
    
    def test_get_current_player(self):
        current = self.game.get_current_player()
        self.assertEqual(current.name, "Juan")
        self.assertEqual(current.color, "white")
    
    def test_get_board(self):
        board = self.game.get_board()
        self.assertIsNotNone(board)
        self.assertEqual(len(board.__pos__), 24)
    
    def test_get_dice(self):
        dice = self.game.get_dice()
        self.assertIsNotNone(dice)
    
    def test_get_players(self):
        players = self.game.get_players()
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "Juan")
        self.assertEqual(players[1].name, "María")
    
    @patch('random.randint', side_effect=[3, 5])
    def test_roll_dice_valid(self, mock_randint):
        self.game.start()
        result = self.game.roll_dice()
        self.assertEqual(result, (3, 5))
    
    def test_roll_dice_not_started(self):
        result = self.game.roll_dice()
        self.assertIsNone(result)

    def test_roll_dice_wrong_turn(self):
        self.game.start()
        with self.assertRaises(NotYourTurnError):
            self.game.__current_player__ = self.game.__player2__
            Player.current_turn = "white"
            self.game.roll_dice()
    
    @patch('random.randint', side_effect=[4, 4])
    def test_roll_dice_double(self, mock_randint):
        self.game.start()
        result = self.game.roll_dice()
        self.assertEqual(result, (4, 4))
        self.assertTrue(self.game.__dice__.is_double())
    
    @patch('random.randint', side_effect=[2, 5])
    def test_get_available_moves(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        available = self.game.get_available_moves()
        self.assertIn(2, available)
        self.assertIn(5, available)
    
    def test_must_enter_from_bar_false(self):
        self.assertFalse(self.game.must_enter_from_bar())
    
    def test_must_enter_from_bar_true(self):
        self.game.__board__.__bar__["white"] = 1
        self.assertTrue(self.game.must_enter_from_bar())
    
    def test_has_pieces_in_home_board_white_false(self):
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[10] = ["white", 2]
        result = self.game.has_pieces_in_home_board("white")
        self.assertFalse(result)
    
    def test_has_pieces_in_home_board_white_true(self):
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[20] = ["white", 2]
        self.game.__board__.__pos__[21] = ["white", 3]
        self.game.__board__.__bar__["white"] = 0
        result = self.game.has_pieces_in_home_board("white")
        self.assertTrue(result)
    
    def test_has_pieces_in_home_board_black_true(self):
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[3] = ["black", 2]
        self.game.__board__.__pos__[4] = ["black", 3]
        self.game.__board__.__bar__["black"] = 0
        result = self.game.has_pieces_in_home_board("black")
        self.assertTrue(result)
    
    def test_validate_move_distance_white_valid(self):
        self.game.__dice__.__values__ = [3, 5]
        result = self.game.validate_move_distance(10, 13, "white")
        self.assertTrue(result)
    
    def test_validate_move_distance_white_invalid(self):
        self.game.__dice__.__values__ = [3, 5]
        result = self.game.validate_move_distance(10, 12, "white")
        self.assertFalse(result)