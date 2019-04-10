# -------------- main.py  -------------- #
# ----------- dependencies  ---------- #

from kivy.config import Config

from application import GameOfLife

# ----------- code  ---------- #
# main function
# to run Game Of Life App

if __name__ == '__main__':

    game = GameOfLife()

    Config.set('graphics', 'width', 1200)
    Config.set('graphics', 'height', 800)
    Config.set('graphics', 'resizable', 0)

    game.run()
