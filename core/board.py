class Board:
    def __init__(self):
        self.positions = {}
        self.bar = {"white": 0, "black": 0}
        self.off_board = {"white": 0, "black": 0}
        self.setup_initial_positions()

    def setup_initial_position(self):
        self.pos = [None for _ in range(24)]
        
        self.pos[0] = ["white", 2]
        self.pos[11] = ["white", 5]
        self.pos[16] = ["white", 3]
        self.pos[18] = ["white", 5]
        
        self.pos[23] = ["black", 2]
        self.pos[12] = ["black", 5]
        self.pos[7] = ["black", 3]
        self.pos[5] = ["black", 5]


    

    