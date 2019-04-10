# -------------- settings.py  -------------- #
# ----------- dependencies  ---------- #

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

# ----------- code  ---------- #
# Settings page allows to:
# change the framerate speed of the animation
# zoom on game board
# upload a pattern from patterns directory


class SettingsScreen(Screen):
    board = ObjectProperty(None)
    game_screen = ObjectProperty(None)

    # references to game widgets
    def bind_game(self, board, game):
        self.board = board
        self.game_screen = game

    # change framerate of animation
    def change_framerate(self, value):
        self.game_screen.speed = 1/value

    # zoom on board board
    def zoom(self, value):
        default_rows = self.board.default_dimensions[0]
        default_cols = self.board.default_dimensions[1]

        if value == 0:
            self.board.zoom(rows=default_rows, cols=default_cols)
        else:
            # max zoom is half of the board
            rows = int(default_rows - default_rows / 100 * (value/2))
            cols = int(default_cols - default_cols / 100 * (value/2))

            if rows != self.board.rows and cols != self.board.cols:
                self.board.zoom(rows=rows, cols=cols)

    # upload on board a pattern from patterns directory
    def upload_pattern(self, file):
        self.board.upload_pattern(file)