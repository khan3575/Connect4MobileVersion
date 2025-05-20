from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

class Cell(Widget):
    # 0=empty, 1=red, 2=yellow
    player = NumericProperty(0)
