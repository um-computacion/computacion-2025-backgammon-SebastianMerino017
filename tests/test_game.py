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

            from core.player import Player as _Player
            _Player.switch_turn()
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

class TestGameMore(unittest.TestCase):
    def setUp(self):
        Player.reset_game()
        self.game = Game("P1", "P2")

    def tearDown(self):
        Player.reset_game()

    def test_move_piece_not_started_raises(self):
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 1)

    def test_move_piece_not_your_turn_raises(self):
        self.game.start()

        Player.current_turn = 'black'
        with self.assertRaises(NotYourTurnError):
            self.game.move_piece(0, 1)

    def test_move_piece_invalid_types(self):
        self.game.start()
        Player.current_turn = 'white'
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece('a', 1)

    def test_move_piece_out_of_range(self):
        self.game.start()
        Player.current_turn = 'white'
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(-1, 100)

    def test_move_piece_bar_present(self):
        self.game.start()
        Player.current_turn = 'white'

        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 1, 'black': 0}, 'off_board': {}
        })
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 1)

    def test_move_piece_no_dice(self):
        self.game.start()
        Player.current_turn = 'white'

        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })

        dice = MagicMock()
        dice.has_available_values.return_value = False
        self.game.__dice__ = dice
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 1)

    def test_move_piece_distance_not_available(self):
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        dice.get_available_values.return_value = [1, 2]
        self.game.__dice__ = dice
 
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 3)

    def test_move_piece_wrong_direction(self):
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        dice.get_available_values.return_value = [3]
        self.game.__dice__ = dice

        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(5, 2)

    def test_move_piece_board_invalid_move(self):
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        dice.get_available_values.return_value = [3]
        self.game.__dice__ = dice
  
        self.game.__board__.is_valid_move = MagicMock(return_value=False)
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 3)

    def test_move_piece_success(self):
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        dice.get_available_values.return_value = [3]
        dice.use_value.return_value = True
        self.game.__dice__ = dice
  
        self.game.__board__.is_valid_move = MagicMock(return_value=True)

        self.game.__board__.move_piece = MagicMock(return_value=True)
        res = self.game.move_piece(0, 3)
        self.assertTrue(res)
        self.game.__board__.move_piece.assert_called()

    def test_enter_from_bar_success(self):
        self.game.start()
        Player.current_turn = 'white'
 
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 1, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        self.game.__dice__ = dice

        self.assertTrue(self.game.enter_from_bar(18))

    def test_bear_off_success(self):
        self.game.start()
        Player.current_turn = 'white'
  
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = True
        self.game.__dice__ = dice
        self.assertTrue(self.game.bear_off(18))

    def test_end_turn_requires_rolled(self):
        self.game.start()
        Player.current_turn = 'white'

        with self.assertRaises(InvalidMoveError):
            self.game.end_turn()

class TestGameExtra(unittest.TestCase):
    def setUp(self):
        Player.reset_game()
        self.game = Game("A", "B")

    def tearDown(self):
        Player.reset_game()

    def test_get_game_state_defaults(self):
        state = self.game.get_game_state()
        self.assertIn('board', state)
        self.assertIn('dice', state)
        self.assertIn('current_player', state)
        self.assertFalse(state['started'])

    def test_is_game_over_sets_winner(self):
 
        Player.game_pieces['white']['off_board'] = 15
        over = self.game.is_game_over()
        self.assertTrue(over)
        self.assertIsNotNone(self.game.get_winner())

    def test_roll_dice_before_start(self):

        res = self.game.roll_dice()
        self.assertIsNone(res)

    def test_enter_from_bar_no_pieces(self):
        self.game.start()
        with self.assertRaises(NoPiecesInBarError):
            self.game.enter_from_bar(18)

    def test_bear_off_not_started(self):
        with self.assertRaises(InvalidMoveError):
            self.game.bear_off(18)

class TestGameCoverage(unittest.TestCase):
    def setUp(self):
        Player.reset_game()
        self.game = Game("X", "Y")

    def tearDown(self):
        Player.reset_game()

    def test_start_already_started(self):
        """Cubre el caso en que el juego ya está iniciado."""
        self.game.start()
        result = self.game.start()
        self.assertTrue(result) 

    @patch('random.randint', side_effect=[4, 4])  
    def test_roll_dice_double(self, mock_randint):
        """Verifica que el doble se maneje correctamente."""
        self.game.start()
        result = self.game.roll_dice()
        dice_values = self.game.get_dice().get_values()
        self.assertEqual(dice_values, [4, 4, 4, 4])
        self.assertIsNotNone(result)

    @patch('random.randint', side_effect=[3, 5])
    def test_end_turn_with_dice_left(self, mock_randint):
        """Cubre intento de terminar turno con dados aún disponibles."""
        self.game.start()
        self.game.roll_dice()
        self.game._Game__dice_rolled__ = True
        with patch.object(self.game.get_dice(), 'has_available_values', return_value=True):
            with self.assertRaises(InvalidMoveError):
                self.game.end_turn()

    def test_is_game_over_no_winner(self):
        """Cubre el caso en que ningún jugador ha ganado."""
        Player.game_pieces['white']['off_board'] = 10
        Player.game_pieces['black']['off_board'] = 5
        result = self.game.is_game_over()
        self.assertFalse(result)
        self.assertIsNone(self.game.get_winner())

    def test_get_game_state_after_start(self):
        """Cubre el estado del juego una vez iniciado."""
        self.game.start()
        state = self.game.get_game_state()
        self.assertTrue(state['started'])
        self.assertEqual(state['current_player'], 'white')

    def test_enter_from_bar_no_dice_values(self):
        """Hay piezas en bar pero no valores válidos de dado."""
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 1, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = False
        self.game.__dice__ = dice
        with self.assertRaises(InvalidMoveError):
            self.game.enter_from_bar(20)

    def test_bear_off_no_dice_values(self):
        """Intento de bear_off sin dados disponibles."""
        self.game.start()
        Player.current_turn = 'white'
        self.game.__board__.get_state = MagicMock(return_value={
            'positions': [], 'bar': {'white': 0, 'black': 0}, 'off_board': {}
        })
        dice = MagicMock()
        dice.has_available_values.return_value = False
        self.game.__dice__ = dice
        with self.assertRaises(InvalidMoveError):
            self.game.bear_off(20)

if __name__ == '__main__':
    unittest.main()