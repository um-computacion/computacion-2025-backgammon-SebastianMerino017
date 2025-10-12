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

    def test_validate_move_distance_black_valid(self):
        self.game.__dice__.__values__ = [3, 5]
        result = self.game.validate_move_distance(13, 10, "black")
        self.assertTrue(result)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_move_piece_valid(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__[0] = ["white", 2]
        self.game.__board__.__pos__[3] = None
        
        result = self.game.move_piece(0, 3)
        self.assertTrue(result)
        self.assertEqual(self.game.__board__.__pos__[3], ["white", 1])
    
    def test_move_piece_not_your_turn(self):
        self.game.start()
        self.game.__current_player__ = self.game.__player2__
        Player.current_turn = "white"
        
        with self.assertRaises(NotYourTurnError):
            self.game.move_piece(0, 3)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_move_piece_no_dice_available(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        self.game.__dice__.use_value(3)
        self.game.__dice__.use_value(5)
        
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 3)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_move_piece_must_enter_from_bar(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        self.game.__board__.__bar__["white"] = 1
        
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 3)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_move_piece_invalid_position(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 25)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_move_piece_wrong_distance(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__[0] = ["white", 2]
        
        with self.assertRaises(InvalidMoveError):
            self.game.move_piece(0, 2)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_enter_from_bar_valid_white(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__bar__["white"] = 1
        self.game.__board__.__pos__[21] = None
        
        result = self.game.enter_from_bar(21)
        self.assertTrue(result)
        self.assertEqual(self.game.__board__.__bar__["white"], 0)
        self.assertEqual(self.game.__board__.__pos__[21], ["white", 1])
    
    def test_enter_from_bar_no_pieces(self):
        self.game.start()
        
        with self.assertRaises(NoPiecesInBarError):
            self.game.enter_from_bar(20)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_enter_from_bar_not_your_turn(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        self.game.__board__.__bar__["white"] = 1
        self.game.__current_player__ = self.game.__player2__
        Player.current_turn = "white"
        
        with self.assertRaises(NotYourTurnError):
            self.game.enter_from_bar(20)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_enter_from_bar_wrong_zone(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        self.game.__board__.__bar__["white"] = 1
        
        with self.assertRaises(InvalidMoveError):
            self.game.enter_from_bar(10)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_bear_off_valid(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[20] = ["white", 2]
        self.game.__board__.__pos__[21] = ["white", 3]
        self.game.__board__.__bar__["white"] = 0
        Player.game_pieces["white"]["on_board"] = 5
        
        result = self.game.bear_off(21)
        self.assertTrue(result)
        self.assertEqual(self.game.__board__.__pos__[21], ["white", 2])
        self.assertEqual(Player.game_pieces["white"]["off_board"], 1)
    
    def test_bear_off_not_your_turn(self):
        self.game.start()
        self.game.__current_player__ = self.game.__player2__
        Player.current_turn = "white"
        
        with self.assertRaises(NotYourTurnError):
            self.game.bear_off(20)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_bear_off_must_enter_from_bar(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        self.game.__board__.__bar__["white"] = 1
        
        with self.assertRaises(InvalidMoveError):
            self.game.bear_off(20)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_bear_off_not_all_in_home(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__[10] = ["white", 2]
        
        with self.assertRaises(InvalidMoveError):
            self.game.bear_off(20)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_bear_off_wrong_position(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[20] = ["white", 2]
        
        with self.assertRaises(InvalidMoveError):
            self.game.bear_off(10)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_end_turn_valid(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        initial_player = self.game.get_current_player()
        result = self.game.end_turn()
        
        self.assertTrue(result)
        self.assertNotEqual(self.game.get_current_player(), initial_player)
    
    def test_end_turn_not_your_turn(self):
        self.game.start()
        self.game.__current_player__ = self.game.__player2__
        Player.current_turn = "white"
        
        with self.assertRaises(NotYourTurnError):
            self.game.end_turn()
    
    def test_get_winner_none(self):
        self.assertIsNone(self.game.get_winner())
    
    def test_get_winner_exists(self):
        self.game.__winner__ = self.game.__player1__
        winner = self.game.get_winner()
        self.assertEqual(winner.name, "Juan")
    
    def test_is_game_over_false(self):
        self.assertFalse(self.game.is_game_over())
    
    def test_is_game_over_true(self):
        self.game.__winner__ = self.game.__player1__
        self.assertTrue(self.game.is_game_over())
    
    @patch('random.randint', side_effect=[3, 5])
    def test_get_game_state(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        state = self.game.get_game_state()
        
        self.assertIn("board", state)
        self.assertIn("player1", state)
        self.assertIn("player2", state)
        self.assertIn("current_player", state)
        self.assertIn("dice", state)
        self.assertIn("winner", state)
        self.assertIn("game_started", state)
        
        self.assertEqual(state["current_player"], "Juan")
        self.assertTrue(state["game_started"])
        self.assertIsNone(state["winner"])
    
    def test_str_not_started(self):
        result = str(self.game)
        self.assertIn("No iniciado", result)
        self.assertIn("Juan", result)
    
    def test_str_started(self):
        self.game.start()
        result = str(self.game)
        self.assertIn("Iniciado", result)
        self.assertIn("Juan", result)
    
    @patch('random.randint', side_effect=[3, 5])
    def test_complete_turn_flow(self, mock_randint):
        self.game.start()
        
        self.assertEqual(self.game.get_current_player().name, "Juan")
        
        dice = self.game.roll_dice()
        self.assertEqual(dice, (3, 5))
        
        available = self.game.get_available_moves()
        self.assertEqual(len(available), 2)
        
        self.game.__board__.__pos__[0] = ["white", 2]
        self.game.__board__.__pos__[3] = None
        self.game.move_piece(0, 3)
        
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().name, "María")
    
    @patch('random.randint', side_effect=[6, 6, 1, 2])
    def test_bear_off_win_condition(self, mock_randint):
        self.game.start()
        self.game.roll_dice()
        
        self.game.__board__.__pos__ = [None for _ in range(24)]
        self.game.__board__.__pos__[23] = ["white", 1]
        self.game.__board__.__bar__["white"] = 0
        Player.game_pieces["white"]["on_board"] = 1
        Player.game_pieces["white"]["off_board"] = 14
        
        self.game.bear_off(23)
        
        self.assertTrue(self.game.is_game_over())
        self.assertIsNotNone(self.game.get_winner())
        self.assertEqual(self.game.get_winner().name, "Juan")


if __name__ == '__main__':
    unittest.main(verbosity=2)