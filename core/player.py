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