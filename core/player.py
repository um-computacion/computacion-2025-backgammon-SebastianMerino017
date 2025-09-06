import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pices = 15
        self.pices_on_board = 15
        self.pices_off_board = 0
        self.is_dead = False
        self.score = 0

    def __str__(self):
        return f"Jugador: {self.name} ({self.color})"
    
    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        return dice1, dice2

    def get_possible_moves(self, dice_values, board_state):
        possible_moves = []
        
        if dice_values[0] == dice_values[1]:
            moves = [dice_values[0]]*4
        else:
            moves = dice_values.copy()

        return moves
    
