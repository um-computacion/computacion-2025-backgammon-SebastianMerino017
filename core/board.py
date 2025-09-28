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


    def draw(self):
        result_board = [] 
        for col in range(11, -1, -1):
            result_row = []
            result_board.append(result_row)
            for row in range(0, 5):
                if self.pos[col] is not None:
                    if self.pos[col][1] > row:
                        if row < 4:
                            piece = self.get_piece(col)
                        else:
                            if self.pos[col][1] <= 5:
                                piece = self.get_piece(col)
                            else:
                                piece = str(self.pos[col][1] - 4)
                        result_row.append(piece)
                    else:
                        result_row.append(' ')    
                else:
                    result_row.append(' ')
        return result_board

    def get_piece(self, col):
        if self.pos[col][0] == 'white':
            return 'W'
        else:
            return 'B'

    