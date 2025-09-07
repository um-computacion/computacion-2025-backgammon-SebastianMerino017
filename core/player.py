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
    
    def make_move(self, from_position, to_position):
        print(f"{self.name} ha hecho el movimiento de {from_position} a {to_position}")
        return True
    
    def can_bear_off(self, board_state):
        if self.color == "white":
            home_positions = range(19, 25)

        else: 
            home_positions = range(1, 7)

        pieces_in_home = 0
        for position in home_positions:
            if position in board_state and board_state[position]["color"] == self.color:
                pieces_in_home += board_state[position]["count"]

        total_accounted = pieces_in_home + self.pices_off_board

        return total_accounted == 15
    
    def bear_off_piece(self):
        if self.pieces_on_board > 0:
            self.pices_off_board += 1
            self.pieces_on_board -= 1
    
    def is_winner(self):
        return self.pices_on_board == 15
    
    def resert_for_new_game(self):
        self.pices_on_board = 15
        self.pices_off_board = 0
        self.is_dead = False

    def get_status(self):
        return {
            "name": self.name,
            "color": self.color,
            "pices": self.pices,
            "pices_on_board": self.pices_on_board,
            "pices_off_board": self.pices_off_board,
            "is_dead": self.is_dead,
            "score": self.score
        }
    
if __name__ == "main":
    player1 = Player("Juan", "white")
    player2 = Player("Maria", "black")

    print(player1)
    print(player2)


    