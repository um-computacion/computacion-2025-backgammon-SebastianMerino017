import random

class Player:
    current_turn = None
    turn_counter = 0
    game_pieces = {
        'white': {'on_board': 15, 'off_board': 0},
        'black': {'on_board': 15, 'off_board': 0}
    }

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0

        if Player.current_turn is None:
            Player.current_turn = "white"

    def __str__(self):
        return f"{self.name} ({self.color})"

    @classmethod
    def switch_turn(cls):
        cls.turn_counter += 1
        cls.current_turn = "black" if cls.current_turn == "white" else "white"

    @classmethod
    def reset_game(cls):
        cls.current_turn = "white"
        cls.turn_counter = 0
        cls.game_pieces = {
            'white': {'on_board': 15, 'off_board': 0},
            'black': {'on_board': 15, 'off_board': 0}
        }

    def is_my_turn(self):
        return Player.current_turn == self.color

    def end_turn(self):
        if self.is_my_turn():
            Player.switch_turn()

    def roll_dice(self):
        if not self.is_my_turn():
            return None
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return [d1, d2]

    def play_dice(self, dice: list[int]) -> bool:
        """Guardar los valores de los dados solo si es su turno"""
        if not self.is_my_turn():
            return False
        self.dice = dice
        return True

    def bear_off_piece(self):
        if not self.is_my_turn():
            return False
        if Player.game_pieces[self.color]['on_board'] > 0:
            Player.game_pieces[self.color]['on_board'] -= 1
            Player.game_pieces[self.color]['off_board'] += 1
            return True
        return False

    def is_winner(self):
        return Player.game_pieces[self.color]['off_board'] == 15

    def get_pieces_count(self):
        return Player.game_pieces[self.color].copy()

    def get_status(self):
        return {
            'name': self.name,
            'color': self.color,
            'is_my_turn': self.is_my_turn(),
            'pieces': self.get_pieces_count(),
            'score': self.score
        }

