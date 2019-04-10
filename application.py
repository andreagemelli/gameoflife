# -------------- application.py  -------------- #
# ----------- dependencies  ---------- #

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from game import GameLayout
from settings import SettingsScreen

# ----------- code  ---------- #
# Game Of Life application
# kivy app class


class GameOfLife(App):

    def build(self):
        Builder.load_file("layout.kv")  # load the layout of application

        game = GameLayout(name='game')
        game.board.build()

        settings = SettingsScreen(name='settings')
        settings.bind_game(game.board, game)

        sm = ScreenManager()
        sm.add_widget(game)
        sm.add_widget(settings)

        return sm