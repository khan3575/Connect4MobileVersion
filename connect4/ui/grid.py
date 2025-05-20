from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from game.board import Board
from kivy.properties import ObjectProperty

class GameGrid(GridLayout):
    app = ObjectProperty()

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        # figure out which column was tapped
        col = int((touch.x - self.x) / self.width * Board.COLS)
        drop = self.app.board.drop(col)
        if drop:
            r, c = drop
            cell = self.app.cells[r][c]
            cell.player = self.app.board.current

            # animate drop from top of grid into position
            cell.y = self.y + self.height  # start above
            Animation(y=(self.y + (Board.ROWS-1-r)*(self.height/Board.ROWS)),
                      d=0.5, t='out_bounce').start(cell)

            if self.app.board.check_win(r, c):
                self.app.show_win(self.app.board.current)
            else:
                self.app.board.switch()
                self.app.update_header()
        return True
