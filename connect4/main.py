# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.metrics import dp

from game.board import Board
from ui.cell import Cell
from ui.grid import GameGrid

# Set window size for testing
Window.size = (420, 700)

# Load the screens KV file
Builder.load_file('ui/screens.kv')

class Connect4App(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('user_store.json')
        self.current_user = "Guest"
        self.board = None
        self.cells = []  # 2D list for cell widgets
        self.winner_cells = []

    def build(self):
        # Build the screen manager with defined screens
        return Builder.load_string('''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    MenuScreen:
    GameScreen:
    StatsScreen:
        ''')

    # User Authentication Methods
    def register_user(self, u, p):
        if not u or not p:
            return False, 'Username and password required'
            
        if self.store.exists(u):
            return False, 'Username already exists'
            
        self.store.put(u, password=p, wins=0, losses=0, draws=0)
        return True, 'Registration successful!'

    def login_user(self, u, p):
        if not u or not p:
            return False, 'Username and password required'
            
        if not self.store.exists(u):
            return False, 'User does not exist'
            
        data = self.store.get(u)
        if data['password'] != p:
            return False, 'Incorrect password'
            
        self.current_user = u
        return True, 'Login successful!'

    def do_login(self, u, p):
        ok, msg = self.login_user(u, p)
        screen = self.root.get_screen('LoginScreen')
        screen.ids.err.text = msg
        
        if ok:
            # Clear fields
            screen.ids.username_field.text_input.text = ""
            screen.ids.password_field.text_input.text = ""
            # Delayed navigation (feels smoother)
            Clock.schedule_once(lambda dt: self.go_to_menu(), 0.5)

    def do_register(self, u, p):
        ok, msg = self.register_user(u, p)
        screen = self.root.get_screen('RegisterScreen')
        screen.ids.err.text = msg
        
        if ok:
            # Clear fields
            screen.ids.username_field.text_input.text = ""
            screen.ids.password_field.text_input.text = ""
            # Delayed navigation (feels smoother)
            Clock.schedule_once(lambda dt: self.go_to_login(), 0.5)

    # Navigation Methods
    def go_to_register(self):
        self.root.current = 'RegisterScreen'
        screen = self.root.get_screen('RegisterScreen')
        screen.ids.err.text = ""

    def go_to_login(self):
        self.root.current = 'LoginScreen'
        screen = self.root.get_screen('LoginScreen')
        screen.ids.err.text = ""

    def go_to_menu(self):
        self.root.current = 'MenuScreen'

    def go_to_game(self):
        self.root.current = 'GameScreen'
        self.start_game()

    def go_to_stats(self):
        self.update_stats()
        self.root.current = 'StatsScreen'

    def update_stats(self):
        if self.current_user and self.store.exists(self.current_user):
            data = self.store.get(self.current_user)
            screen = self.root.get_screen('StatsScreen')
            screen.ids.win_label.text = str(data.get('wins', 0))
            screen.ids.loss_label.text = str(data.get('losses', 0))
            
            # Calculate win rate
            wins = data.get('wins', 0)
            losses = data.get('losses', 0)
            draws = data.get('draws', 0)
            total = wins + losses + draws
            
            if total > 0:
                win_rate = (wins / total) * 100
                screen.ids.win_rate_label.text = f"{win_rate:.1f}%"
            else:
                screen.ids.win_rate_label.text = "0%"

    # Game Flow Methods
    def start_game(self):
        self.board = Board()
        screen = self.root.get_screen('GameScreen')
        screen.ids.header.text = f"Player {self.board.current}'s Turn"  # FIXED: Use ids.header
        self.cells = []  # Reset cells array

        # Clear any previous widgets
        screen.ids.gamegrid.clear_widgets()

        # Create grid of Cell widgets (6 rows x 7 columns)
        for r in range(Board.ROWS):
            row_cells = []
            for c in range(Board.COLS):
                cell = Cell()
                row_cells.append(cell)
                screen.ids.gamegrid.add_widget(cell)
            self.cells.append(row_cells)

    def update_header(self):
        self.root.get_screen('GameScreen').ids.header.text = f"Player {self.board.current}'s Turn"  # FIXED: Use ids.header

    def show_win(self, winner, winning_cells):
        # Update stats for the current user
        if self.store.exists(self.current_user):
            data = self.store.get(self.current_user)
            data['wins'] = data.get('wins', 0) + 1
            self.store.put(self.current_user, **data)
        
        # Highlight winning cells
        for r, c in winning_cells:
            self.cells[r][c].pulse()
            
        # Create and show the winner popup
        popup = Factory.WinPopup()
        popup.ids.win_title.text = "Victory!"
        popup.ids.win_message.text = f"Player {winner} Wins!"
        
        if winner == 1:
            popup.ids.win_message.color = (0.9, 0.2, 0.2, 1)  # Red
        else:
            popup.ids.win_message.color = (0.9, 0.9, 0.2, 1)  # Yellow
            
        popup.open()

    def show_draw(self):
        # Update stats for the current user
        if self.store.exists(self.current_user):
            data = self.store.get(self.current_user)
            data['draws'] = data.get('draws', 0) + 1
            self.store.put(self.current_user, **data)
        
        # Create and show the draw popup
        popup = Factory.WinPopup()
        popup.ids.win_title.text = "Game Over"
        popup.ids.win_message.text = "It's a Draw!"
        popup.ids.win_message.color = (0.7, 0.7, 0.7, 1)  # Gray
        popup.open()

    def restart_game(self):
        self.go_to_game()

if __name__ == '__main__':
    Connect4App().run()