class Board:
    def __init__(self):
        self.positions = {}
        self.bar = {"white": 0, "black": 0}
        self.off_board = {"white": 0, "black": 0}
        self.setup_initial_position()

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
        
    def draw_full_board(self):
        upper_board = []
        for col in range(12, 24):
            result_row = []
            upper_board.append(result_row)
            
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
        
        lower_board = []
        for col in range(11, -1, -1):
            result_row = []
            lower_board.append(result_row)
            
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
        
        return {"upper": upper_board, "lower": lower_board}
    
    def get_piece(self, col):
        if self.pos[col][0] == 'white':
            return 'W'
        else:
            return 'B'

    def display_board_console(self):
        print("=" * 50)
        print("         TABLERO DE BACKGAMMON")
        print("=" * 50)
        
        print(f"Barra -> Blanco: {self.bar['white']}, Negro: {self.bar['black']}")
        print()
        
        print("Posiciones 13-24:")
        for i in range(12, 24):
            if self.pos[i] is not None:
                color = "W" if self.pos[i][0] == "white" else "B"
                count = self.pos[i][1]
                print(f"{i+1:2d}: {color}{count}", end="  ")
            else:
                print(f"{i+1:2d}: --", end="  ")
            
            if i == 17:
                print("| ", end="")
        
        print("\n" + "-" * 50)
        
        print("Posiciones 12-1:")
        for i in range(11, -1, -1):
            if self.pos[i] is not None:
                color = "W" if self.pos[i][0] == "white" else "B"
                count = self.pos[i][1]
                print(f"{i+1:2d}: {color}{count}", end="  ")
            else:
                print(f"{i+1:2d}: --", end="  ")
            
            if i == 6:
                print("| ", end="")
        
        print()
        print(f"\nFichas fuera del tablero -> Blanco: {self.off_board['white']}, Negro: {self.off_board['black']}")
        print("=" * 50)

    def is_valid_position(self, pos):
        return isinstance(pos, int) and 0 <= pos <= 23
    
    def get_position_info(self, pos):
        if not self.is_valid_position(pos):
            return None
        return self.pos[pos]
    
    def can_place_piece(self, pos, color):
        if not self.is_valid_position(pos):
            return False
        
        if self.pos[pos] is None:
            return True
        
        if self.pos[pos][0] == color:
            return True
        
        if self.pos[pos][1] == 1:
            return True
        
        return False
    
    def move_piece(self, from_pos, to_pos, color):
        if not self.is_valid_position(from_pos) or not self.is_valid_position(to_pos):
            return False
        
        if self.pos[from_pos] is None or self.pos[from_pos][0] != color:
            return False
        
        if not self.can_place_piece(to_pos, color):
            return False
        
        if self.pos[to_pos] is not None and self.pos[to_pos][0] != color:
            enemy_color = self.pos[to_pos][0]
            self.bar[enemy_color] += 1
            self.pos[to_pos] = None
        
        self.pos[from_pos][1] -= 1
        if self.pos[from_pos][1] == 0:
            self.pos[from_pos] = None
        
        if self.pos[to_pos] is None:
            self.pos[to_pos] = [color, 1]
        else:
            self.pos[to_pos][1] += 1
        
        return True
    
    def total_pieces(self, color):
        on_board = sum(pos[1] for pos in self.pos if pos is not None and pos[0] == color)
        in_bar = self.bar[color]
        off = self.off_board[color]
        return on_board + in_bar + off

    

