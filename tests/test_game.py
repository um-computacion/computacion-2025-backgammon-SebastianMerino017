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