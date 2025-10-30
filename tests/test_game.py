import unittest
from unittest.mock import patch, MagicMock
from core.game import Game, InvalidMoveError, NotYourTurnError, NoPiecesInBarError
from core.player import Player


class TestGame(unittest.TestCase):
    
    def setUp(self):
        Player.reset_game()
        self.game = Game("Juan", "María")
    
    def tearDown(self):
        Player.reset_game()
    
    def test_initialization(self):
        self.assertIsNotNone(self.game.get_board())
        players = self.game.get_players()
        self.assertEqual(len(players), 2)
        self.assertIsNotNone(self.game.get_dice())
        self.assertEqual(players[0].name, "Juan")
        self.assertEqual(players[1].name, "María")
        self.assertEqual(players[0].color, "white")
        self.assertEqual(players[1].color, "black")
        self.assertIsNone(self.game.get_winner())
        self.assertFalse(self.game.is_game_over())
    
    def test_start_game(self):
        result = self.game.start()
        self.assertTrue(result)
    
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

    def test_roll_dice_not_your_turn(self):
        self.game.start()
        Player.switch_turn()
        
        with self.assertRaises(NotYourTurnError):
            self.game.roll_dice()

    @patch('random.randint', side_effect=[1, 2, 3, 4])
    def test_end_turn(self, mock_randint):
        self.game.start()
        
        self.game.roll_dice()
        self.game._Game__dice_rolled__ = True
        with patch.object(self.game.get_dice(), 'has_available_values', return_value=False):
            self.game.end_turn()
        current = self.game.get_current_player()
        self.assertEqual(current.name, "María")
        
        self.game.roll_dice()
        self.game._Game__dice_rolled__ = True
        with patch.object(self.game.get_dice(), 'has_available_values', return_value=False):
            self.game.end_turn()
        current = self.game.get_current_player()
        self.assertEqual(current.name, "Juan")
    
    @patch('random.randint', side_effect=[1, 2, 3, 4]) 
    def test_end_turn_not_your_turn(self, mock_randint):
        self.game.start()
        self.game.roll_dice() 
        self.game._Game__dice_rolled__ = True 
        with patch.object(self.game.get_dice(), 'has_available_values', return_value=False):
            self.game.end_turn() 
        
        self.game.roll_dice() 
        self.game._Game__dice_rolled__ = True 
        
        with patch.object(self.game.get_dice(), 'has_available_values', return_value=False):
            with self.assertRaises(NotYourTurnError):
                self.game.end_turn()

    def test_str_representation(self):
        result = str(self.game)
        self.assertIn("No iniciado", result)
        
        self.game.start()
        result = str(self.game)
        self.assertIn("Iniciado", result)
        self.assertIn("Juan", result)
    
    @patch('random.randint', side_effect=[3, 4])
    def test_end_turn_with_available_dice(self, mock_randint):
        self.game.start()
        self.game.roll_dice() 
        self.game._Game__dice_rolled__ = True 
        
        with self.assertRaises(InvalidMoveError):
            self.game.end_turn() 
            
    @patch('random.randint', side_effect=[3, 5])
    def test_roll_dice_after_rolling(self, mock_randint):
        self.game.start()
        self.game.roll_dice() 
        self.game._Game__dice_rolled__ = True 
        
        with self.assertRaises(InvalidMoveError):
            self.game.roll_dice() 

if __name__ == '__main__':
    unittest.main()