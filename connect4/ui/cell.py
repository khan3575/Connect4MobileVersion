# ui/cell.py
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.metrics import dp

class Cell(Widget):
    player = NumericProperty(0)  # 0 = empty, 1 = player 1, 2 = player 2
    
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.bind(player=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(0.1, 0.1, 0.15, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Border
            Color(0.3, 0.3, 0.4, 1)
            Rectangle(pos=self.pos, size=(self.width, dp(2)))  # Top
            Rectangle(pos=self.pos, size=(dp(2), self.height))  # Left
            Rectangle(pos=(self.right - dp(2), self.y), size=(dp(2), self.height))  # Right
            Rectangle(pos=(self.x, self.y), size=(self.width, dp(2)))  # Bottom
            
            # Game piece (circle)
            if self.player != 0:
                # Calculate circle size and position
                circle_size = min(self.width, self.height) * 0.7
                circle_x = self.center_x - circle_size / 2
                circle_y = self.center_y - circle_size / 2
                
                if self.player == 1:
                    Color(0.9, 0.2, 0.2, 1)  # Red for player 1
                else:
                    Color(0.9, 0.9, 0.2, 1)  # Yellow for player 2
                    
                Ellipse(pos=(circle_x, circle_y), size=(circle_size, circle_size))
    
    def animate_drop(self, target_y):
        """Animate the cell falling into place."""
        anim = Animation(y=target_y, duration=0.3, t='out_bounce')
        anim.start(self)
    
    def pulse(self):
        """Pulse animation for winning cells."""
        # Scale up and down
        anim1 = Animation(size=(self.width * 1.1, self.height * 1.1), duration=0.2)
        anim2 = Animation(size=(self.width, self.height), duration=0.2)
        anim = anim1 + anim2
        anim.repeat = True
        anim.start(self)