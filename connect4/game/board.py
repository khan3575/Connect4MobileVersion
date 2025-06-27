# game/board.py
class Board:
    ROWS = 6
    COLS = 7
    
    def __init__(self):
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current = 1  # Player 1 starts
    
    def drop(self, col):
        """Drop a piece in the specified column. Returns (row, col) if successful, None if column is full."""
        if col < 0 or col >= self.COLS:
            return None
            
        # Find the lowest empty row in this column
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = self.current
                return (row, col)
        
        return None  # Column is full
    
    def switch(self):
        """Switch to the other player."""
        self.current = 2 if self.current == 1 else 1
    
    def check_win(self, row, col):
        """Check if the move at (row, col) creates a winning condition."""
        player = self.grid[row][col]
        
        # Check all four directions: horizontal, vertical, diagonal1, diagonal2
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal /
            (1, -1),  # diagonal \
        ]
        
        for dr, dc in directions:
            # Count in both directions from the placed piece
            count = 1  # Count the piece we just placed
            winning_cells = [(row, col)]
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                   self.grid[r][c] == player):
                winning_cells.append((r, c))
                count += 1
                r, c = r + dr, c + dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                   self.grid[r][c] == player):
                winning_cells.append((r, c))
                count += 1
                r, c = r - dr, c - dc
            
            # If we have 4 or more in a row, we have a winner
            if count >= 4:
                return winning_cells
        
        return None  # No win found
    
    def is_full(self):
        """Check if the board is completely full."""
        for col in range(self.COLS):
            if self.grid[0][col] == 0:  # Top row has empty space
                return False
        return True
    
    def get_cell(self, row, col):
        """Get the value at the specified cell."""
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        return None