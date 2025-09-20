class Board:
    def __init__(self):
        self.positions = {}
        self.bar = {"white": 0, "black": 0}
        self.setup_initial_positions()

