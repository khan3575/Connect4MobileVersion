# game/board.py

class Board:
    ROWS, COLS = 6, 7

    def __init__(self):
        self.grid = [[0] * Board.COLS for _ in range(Board.ROWS)]
        self.current = 1
        self.game_over = False
        self.last_move = None

    def drop(self, col):
        if self.game_over:
            return None
            
        for r in range(Board.ROWS - 1, -1, -1):
            if self.grid[r][col] == 0:
                self.grid[r][col] = self.current
                self.last_move = (r, col)
                return r, col
        return None

    def check_win(self, r, c):
        if r is None or c is None:
            return False
            
        player = self.grid[r][c]
        if player == 0:
            return False
            
        # Four directions: vertical, horizontal, diagonal, anti-diagonal
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            winning_cells = [(r, c)]
            
            for sign in (1, -1):
                rr, cc = r + dr * sign, c + dc * sign
                while 0 <= rr < Board.ROWS and 0 <= cc < Board.COLS and self.grid[rr][cc] == player:
                    count += 1
                    winning_cells.append((rr, cc))
                    rr += dr * sign
                    cc += dc * sign
                    
            if count >= 4:
                self.game_over = True
                return winning_cells
                
        return False

    def is_full(self):
        return all(self.grid[0][c] != 0 for c in range(Board.COLS))

    def switch(self):
        self.current = 2 if self.current == 1 else 1

    def reset(self):
        self.grid = [[0] * Board.COLS for _ in range(Board.ROWS)]
        self.current = 1
        self.game_over = False
        self.last_move = None