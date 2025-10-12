class Board:
    def __init__(self):
        self.__pos__ = [None for _ in range(24)]
        self.__bar__ = {"white": 0, "black": 0}
        self.__off_board__ = {"white": 0, "black": 0}
        self.setup_initial_position()

    def setup_initial_position(self):
        self.__pos__ = [None for _ in range(24)]
        
        self.__pos__[0] = ["white", 2]
        self.__pos__[11] = ["white", 5]
        self.__pos__[16] = ["white", 3]
        self.__pos__[18] = ["white", 5]
        
        self.__pos__[23] = ["black", 2]
        self.__pos__[12] = ["black", 5]
        self.__pos__[7] = ["black", 3]
        self.__pos__[5] = ["black", 5]

    def draw(self):
        result_board = [] 
        for col in range(11, -1, -1):
            result_row = []
            result_board.append(result_row)
            for row in range(0, 5):
                if self.__pos__[col] is not None:
                    if self.__pos__[col][1] > row:
                        if row < 4:
                            piece = self.get_piece(col)
                        else:
                            if self.__pos__[col][1] <= 5:
                                piece = self.get_piece(col)
                            else:
                                piece = str(self.__pos__[col][1] - 4)
                        result_row.append(piece)
                    else:
                        result_row.append(' ')    
                else:
                    result_row.append(' ')
        return result_board

    def get_piece(self, col):
        if self.__pos__[col][0] == 'white':
            return 'W'
        else:
            return 'B'
        
    def draw_full_board(self):
        upper_board = []
        for col in range(12, 24):
            result_row = []
            upper_board.append(result_row)
            
            for row in range(0, 5):
                if self.__pos__[col] is not None:
                    if self.__pos__[col][1] > row:
                        if row < 4:
                            piece = self.get_piece(col)
                        else:
                            if self.__pos__[col][1] <= 5:
                                piece = self.get_piece(col)
                            else:
                                piece = str(self.__pos__[col][1] - 4)
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
                if self.__pos__[col] is not None:
                    if self.__pos__[col][1] > row:
                        if row < 4:
                            piece = self.get_piece(col)
                        else:
                            if self.__pos__[col][1] <= 5:
                                piece = self.get_piece(col)
                            else:
                                piece = str(self.__pos__[col][1] - 4)
                        result_row.append(piece)
                    else:
                        result_row.append(' ')
                else:
                    result_row.append(' ')
        
        return {"upper": upper_board, "lower": lower_board}

    def display_board_console(self):
        print("=" * 50)
        print("         TABLERO DE BACKGAMMON")
        print("=" * 50)
        
        print(f"Barra -> Blanco: {self.__bar__['white']}, Negro: {self.__bar__['black']}")
        print()
        
        print("Posiciones 13-24:")
        for i in range(12, 24):
            if self.__pos__[i] is not None:
                color = "W" if self.__pos__[i][0] == "white" else "B"
                count = self.__pos__[i][1]
                print(f"{i+1:2d}: {color}{count}", end="  ")
            else:
                print(f"{i+1:2d}: --", end="  ")
            
            if i == 17:
                print("| ", end="")
        
        print("\n" + "-" * 50)
        
        print("Posiciones 12-1:")
        for i in range(11, -1, -1):
            if self.__pos__[i] is not None:
                color = "W" if self.__pos__[i][0] == "white" else "B"
                count = self.__pos__[i][1]
                print(f"{i+1:2d}: {color}{count}", end="  ")
            else:
                print(f"{i+1:2d}: --", end="  ")
            
            if i == 6:
                print("| ", end="")
        
        print()
        print(f"\nFichas fuera del tablero -> Blanco: {self.__off_board__['white']}, Negro: {self.__off_board__['black']}")
        print("=" * 50)

    def is_valid_position(self, pos):
        return isinstance(pos, int) and 0 <= pos <= 23
    
    def get_position_info(self, pos):
        if not self.is_valid_position(pos):
            return None
        return self.__pos__[pos]
    
    def can_place_piece(self, pos, color):
        if not self.is_valid_position(pos):
            return False
        
        if self.__pos__[pos] is None:
            return True
        
        if self.__pos__[pos][0] == color:
            return True
        
        if self.__pos__[pos][1] == 1:
            return True
        
        return False
    
    def move_piece(self, from_pos, to_pos, color):
        if not self.is_valid_position(from_pos) or not self.is_valid_position(to_pos):
            return False
        
        if self.__pos__[from_pos] is None or self.__pos__[from_pos][0] != color:
            return False
        
        if not self.can_place_piece(to_pos, color):
            return False
        
        if self.__pos__[to_pos] is not None and self.__pos__[to_pos][0] != color:
            enemy_color = self.__pos__[to_pos][0]
            self.__bar__[enemy_color] += 1
            self.__pos__[to_pos] = None
        
        self.__pos__[from_pos][1] -= 1
        if self.__pos__[from_pos][1] == 0:
            self.__pos__[from_pos] = None
        
        if self.__pos__[to_pos] is None:
            self.__pos__[to_pos] = [color, 1]
        else:
            self.__pos__[to_pos][1] += 1
        
        return True
    
    def bear_off(self, pos, color):
        if not self.is_valid_position(pos):
            return False
        
        if self.__pos__[pos] is None or self.__pos__[pos][0] != color:
            return False
        
        if color == "white" and not (18 <= pos <= 23):
            return False
        if color == "black" and not (0 <= pos <= 5):
            return False
        
        self.__pos__[pos][1] -= 1
        if self.__pos__[pos][1] == 0:
            self.__pos__[pos] = None
        
        self.__off_board__[color] += 1
        return True

    def enter_from_bar(self, pos, color):
        if self.__bar__[color] == 0:
            return False
        
        if not self.can_place_piece(pos, color):
            return False
        
        if color == "white" and not (18 <= pos <= 23):
            return False
        if color == "black" and not (0 <= pos <= 5):
            return False
        
        if self.__pos__[pos] is not None and self.__pos__[pos][0] != color:
            enemy_color = self.__pos__[pos][0]
            self.__bar__[enemy_color] += 1
            self.__pos__[pos] = None
        
        self.__bar__[color] -= 1
        if self.__pos__[pos] is None:
            self.__pos__[pos] = [color, 1]
        else:
            self.__pos__[pos][1] += 1
        
        return True
    
    def count_pieces(self, color):
        count = 0
        
        for pos in self.__pos__:
            if pos is not None and pos[0] == color:
                count += pos[1]
        
        count += self.__bar__[color]
        
        return count
    
    def has_pieces_in_home_board(self, color):
        if color == "white":
            home_range = range(18, 24)
        else:
            home_range = range(0, 6)
        
        for pos in range(24):
            if pos not in home_range:
                if self.__pos__[pos] is not None and self.__pos__[pos][0] == color:
                    return False
        
        if self.__bar__[color] > 0:
            return False
        
        return True
    
    def get_state(self):
        return {
            "positions": self.__pos__.copy(),
            "bar": self.__bar__.copy(),
            "off_board": self.__off_board__.copy()
        }
    
    def reset_board(self):
        self.__pos__ = [None for _ in range(24)]
        self.__bar__ = {"white": 0, "black": 0}
        self.__off_board__ = {"white": 0, "black": 0}
        self.setup_initial_position()


if __name__ == "__main__":
    board = Board()

    

