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

    def is_my_turn(self) -> bool:
        return Player.__current_turn__ == self.__color__
    
    def end_turn(self) -> None:
        if self.is_my_turn():
            Player.switch_turn()
