class Board:
    ROWS, COLS = 6, 7

    def __init__(self):
        # 0=empty, 1=Player1, 2=Player2
        self.grid = [[0]*Board.COLS for _ in range(Board.ROWS)]
        self.current = 1

    def drop(self, col):
        """Drop a piece in `col`. Return (row, col) or None if column full."""
        for r in range(Board.ROWS-1, -1, -1):
            if self.grid[r][col] == 0:
                self.grid[r][col] = self.current
                return r, col
        return None

    def check_win(self, r, c):
        """Return True if current player has 4 in a row at (r,c)."""
        player = self.grid[r][c]
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                rr, cc = r + dr*sign, c + dc*sign
                while 0 <= rr < Board.ROWS and 0 <= cc < Board.COLS and self.grid[rr][cc] == player:
                    count += 1
                    rr += dr*sign; cc += dc*sign
            if count >= 4:
                return True
        return False

    def switch(self):
        """Toggle current player (1↔2)."""
        self.current = 2 if self.current == 1 else 1
