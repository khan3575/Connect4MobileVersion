# ui/cell.py
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.graphics import Ellipse, Color, Rectangle, RoundedRectangle, Line
from kivy.animation import Animation
from kivy.metrics import dp

class Cell(Widget):
    player = NumericProperty(0)
    highlighted = BooleanProperty(False)
    bg_color = ListProperty([0.2, 0.2, 0.3, 1])
    
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw background with 3D bevel effect
            if self.highlighted:
                Color(0.9, 0.6, 0.1, 1)  # Highlight color - golden
            else:
                Color(*self.bg_color)
                
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
            
            # Draw the inner hole (empty space)
            padding = min(self.width, self.height) * 0.1
            hole_size = (self.width - padding*2, self.height - padding*2)
            hole_pos = (self.x + padding, self.y + padding)

            # Draw shadow for depth
            Color(0, 0, 0, 0.2)
            Ellipse(pos=(hole_pos[0]-dp(1), hole_pos[1]-dp(1)), 
                   size=(hole_size[0]+dp(2), hole_size[1]+dp(2)))
            
            # Empty hole color
            Color(0.1, 0.1, 0.15, 1)
            Ellipse(pos=hole_pos, size=hole_size)

            # Token display with 3D effect
            if self.player > 0:
                # Token background
                if self.player == 1:
                    # Red token
                    token_color = [0.9, 0.2, 0.2, 1]
                    highlight_color = [1, 0.5, 0.5, 1]
                    shadow_color = [0.5, 0.1, 0.1, 1]
                else:
                    # Yellow token
                    token_color = [0.9, 0.9, 0.2, 1]
                    highlight_color = [1, 1, 0.5, 1]
                    shadow_color = [0.6, 0.6, 0.1, 1]
                
                # Main token
                Color(*token_color)
                Ellipse(pos=hole_pos, size=hole_size)
                
                # Highlight (top-left)
                padding_highlight = padding * 1.3
                highlight_size = (self.width - padding_highlight*2, self.height - padding_highlight*2)
                highlight_pos = (self.x + padding_highlight, self.y + padding_highlight)
                
                Color(*highlight_color)
                Ellipse(pos=highlight_pos, 
                       size=(highlight_size[0]*0.7, highlight_size[1]*0.7),
                       angle_start=45, angle_end=225)
                
                # Shadow (bottom-right)
                Color(*shadow_color)
                Ellipse(pos=highlight_pos, 
                       size=(highlight_size[0]*0.7, highlight_size[1]*0.7),
                       angle_start=225, angle_end=45)
    
    def on_player(self, *args):
        self.update_canvas()
        
    def on_highlighted(self, *args):
        self.update_canvas()
        
    def animate_drop(self, final_y, duration=0.5):
        anim = Animation(y=final_y, d=duration, t='out_bounce')
        anim.start(self)
        
    def pulse(self):
        """Animate a winning cell with a pulsing effect"""
        self.highlighted = True
        anim = Animation(bg_color=[0.9, 0.6, 0.1, 1], d=0.3) + \
               Animation(bg_color=[0.2, 0.2, 0.3, 1], d=0.3)
        anim.repeat = True
        anim.start(self)