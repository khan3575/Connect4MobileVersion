# ui/grid.py
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.metrics import dp
from kivy.clock import Clock
from game.board import Board
from kivy.graphics import Color, Rectangle, Line

class GameGrid(GridLayout):
    app = ObjectProperty()
    hover_col = NumericProperty(-1)
    bg_color = ListProperty([0.15, 0.15, 0.2, 1])
    
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Draw grid background
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)
            
            # Draw column highlight if hovering
            if 0 <= self.hover_col < Board.COLS:
                col_width = self.width / Board.COLS
                highlight_x = self.x + self.hover_col * col_width
                
                Color(0.3, 0.3, 0.4, 1)
                Rectangle(pos=(highlight_x, self.y), 
                          size=(col_width, self.height))

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        
        # Determine the column based on touch position
        relative_x = touch.x - self.x
        col_width = self.width / Board.COLS
        col = int(relative_x / col_width)
        
        # Try to drop a token on the board
        drop = self.app.board.drop(col)
        if drop:
            r, c = drop
            cell = self.app.cells[r][c]
            # Update the cell's player property
            cell.player = self.app.board.current
            
            # Animation: start above the grid and fall into place
            initial_y = self.y + self.height
            final_y = cell.y  # Keep the original position
            cell.y = initial_y
            
            # Add a slight delay for visual interest
            Clock.schedule_once(lambda dt: cell.animate_drop(final_y), 0.05)
            
            # Check for a win
            winning_cells = self.app.board.check_win(r, c)
            if winning_cells:
                self.app.show_win(self.app.board.current, winning_cells)
            elif self.app.board.is_full():
                self.app.show_draw()
            else:
                self.app.board.switch()
                self.app.update_header()
        return True