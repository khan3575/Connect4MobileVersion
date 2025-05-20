from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from game.board import Board
from ui.cell import Cell
from ui.grid import GameGrid
from kivy.uix.popup  import Popup


# now that __init__.py re-exports them, these work:
from game    import Board
from ui      import Cell, GameGrid


class Connect4App(App):
    def build(self):
        # 1) Load only the Cell & GameGrid rules from KV
        Builder.load_file('ui/screens.kv')

        # 2) Create the vertical root container
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 3) Header label
        self.header = Label(
            text="Player 1's turn",
            size_hint_y=0.1,
            font_size='20sp',
            bold=True,
            color=(1,1,1,1)
        )
        root.add_widget(self.header)

        # 4) Game grid
        grid = GameGrid(rows=Board.ROWS, cols=Board.COLS, spacing=4, padding=4)
        grid.app = self  # so it can call back into our App
        self.cells = []
        for r in range(Board.ROWS):
            row = []
            for c in range(Board.COLS):
                cell = Cell()
                grid.add_widget(cell)
                row.append(cell)
            self.cells.append(row)
        root.add_widget(grid)

        # 5) Initialize logic
        self.board = Board()
        return root

    def update_header(self):
        self.header.text = f"Player {self.board.current}'s turn"

    def show_win(self, p):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"Player {p} wins!", font_size='18sp'))
        popup = Popup(
            title='Game Over', content=content,
            size_hint=(0.6, 0.4), auto_dismiss=True
        )
        popup.bind(on_dismiss=lambda *_: self.reset())
        popup.open()

    def reset(self):
        self.board = Board()
        for row in self.cells:
            for cell in row:
                cell.player = 0
        self.update_header()

if __name__ == '__main__':
    Connect4App().run()
