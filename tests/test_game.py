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
    
    def test_get_dice(self):
        dice = self.game.get_dice()
        self.assertIsNotNone(dice)
    
    def test_get_players(self):
        players = self.game.get_players()
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "Juan")
    
    def test_roll_dice_not_started(self):
        result = self.game.roll_dice()
        self.assertIsNone(result)
    
    def test_roll_dice_not_your_turn(self):
        self.game.start()
        self.game.end_turn()
        
        with self.assertRaises(NotYourTurnError) as context:
            self.game.roll_dice()
        self.assertIn("No es el turno de Juan", str(context.exception))

    def test_end_turn(self):
        self.game.start()
        self.game.end_turn()
        current = self.game.get_current_player()
        self.assertEqual(current.name, "María")
        
        self.game.end_turn()
        current = self.game.get_current_player()
        self.assertEqual(current.name, "Juan")
    
    def test_end_turn_not_your_turn(self):
        self.game.start()
        self.game.end_turn()
        
        with self.assertRaises(NotYourTurnError) as context:
            self.game.end_turn()
        self.assertIn("No es el turno de Juan", str(context.exception))

    def test_str_representation(self):
        result = str(self.game)
        self.assertIn("No iniciado", result)
        
        self.game.start()
        result = str(self.game)
        self.assertIn("Iniciado", result)
        self.assertIn("Juan", result)
    
    def test_move_piece_before_rolling_dice(self):
        self.game.start()
        
        with self.assertRaises(InvalidMoveError) as context:
            self.game.move_piece(0, 3)
        
        self.assertIn("Debes tirar los dados", str(context.exception))

    def test_move_piece_from_bar_when_empty(self):
        self.game.start()
        with patch('random.randint', side_effect=[1, 2]):
            self.game.roll_dice()
        
        with self.assertRaises(InvalidMoveError) as context:
            self.game.move_piece('bar_white', 3)
        
        self.assertIn("No tienes piezas en la barra", str(context.exception))

    @patch('random.randint', side_effect=[3, 4])
    def test_end_turn_with_available_dice(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        with self.assertRaises(InvalidMoveError) as context:
            self.game.end_turn()
            
        self.assertIn("Aún tienes dados por usar", str(context.exception))

    @patch('random.randint', side_effect=[3, 5])
    def test_roll_dice_after_rolling(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        with self.assertRaises(InvalidMoveError) as context:
            self.game.roll_dice()
        self.assertIn("Ya has tirado los dados", str(context.exception))

    @patch('random.randint', side_effect=[6, 6, 1, 2])
    def test_bear_off_win_condition(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[23] = ["white", 1]
        self.game.__board__.__bar__["white"] = 0
        Player.game_pieces["white"]["on_board"] = 1
        Player.game_pieces["white"]["off_board"] = 14
        
        self.game.move_piece_bear_off(23)
        
        self.assertTrue(self.game.__player1__.is_winner())
        self.assertEqual(self.game.get_winner(), self.game.__player1__)

if __name__ == '__main__':
    unittest.main()