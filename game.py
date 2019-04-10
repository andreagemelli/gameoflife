# -------------- game.py  -------------- #
# ----------- dependencies  ---------- #

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

import random

from utility.RLEDecoder import RLEDecoder

# ----------- code  ---------- #
# Three classes in this file:
# 1. Cell button class, a widget for each cell of the game grid board
# 2. GameBoard gridlayout class, a widget for the game grid board
# 3. GameLayout screen class, a widget containing everything in the main screen of the application


# -- grid cell widget -- #
class Cell(Button):
    status = 0  # 0 death, 1 alive
    next_status = 0  # status to apply after progress
    generation = 0  # how many steps the cell has been alive
    neighbors = []

    def __init__(self):
        Button.__init__(self)

        # random initialization of cell status
        self.status = random.randint(0, 1)
        if self.status == 0:
            self.background_color = 1, 1, 1, 1
        else:
            self.next_status = self.status
            self.generation = 1
            self.background_color = 0, 0, 0, 1

    # find, for each cell, the eight neighbours around it
    def set_neighbors(self, x, y, grid):
        self.neighbors = []
        for i in [-1, 0, +1]:
            for j in [-1, 0, +1]:
                if i == 0 and j == 0:
                    continue
                try:
                    if (x+i) > 0 and (y+i) > 0:
                        self.neighbors.append(grid[x+i][y+j])
                except IndexError: continue

    # edit the cell clicking on it
    def on_press(self):
        # make the cell alive
        if self.status == 0:
            self.background_color = 0, 0, 0, 1
            self.status = 1
        else:
            # make the cell dead
            self.background_color = 1, 1, 1, 1
            self.status = 0

    # make progresses following the game rules
    def progress(self):
        neighbours_alive = sum(cell.status for cell in self.neighbors)

        # the cell dies by isolation or overcrowding
        if (2 > neighbours_alive or 3 < neighbours_alive) and self.status == 1:
            self.next_status = 0
            self.generation = 0

        # the cell is born by reproduction
        if 3 == neighbours_alive and self.status == 0:
            self.next_status = 1
            self.generation = 1

        # the cell survives, passing to the next generation
        if (3 == neighbours_alive or 2 == neighbours_alive) and self.status == 1:
            self.next_status = 1
            self.generation += 1

    # apply the progresses previously evaluated
    def apply(self):
        self.status = self.next_status

        if self.status == 0:
            self.background_color = 1, 1, 1, 1

        elif self.status == 1:
            r = 0.1 * (self.generation - 1)
            b = 1 / self.generation
            self.background_color = r, 0, b, 1


# -- game board widget -- #
class GameBoard(GridLayout):
    step = NumericProperty(0)  # counter of animation steps
    default_dimensions = [38, 68]  # default board dimensions
    grid = []  # list of all cells widgets
    decorder = RLEDecoder()  # class used to decode rle patterns files and upload them on board

    # build the game board
    def build(self):
        self.rows = self.default_dimensions[0]
        self.cols = self.default_dimensions[1]
        self.grid = [[Cell() for j in range(self.cols)] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.add_widget(self.grid[i][j])
                self.grid[i][j].set_neighbors(i, j, self.grid)

    # zoom the game board
    def zoom(self, rows=default_dimensions[0], cols=default_dimensions[1]):
        self.clear_widgets()
        self.rows = rows
        self.cols = cols

        rows_gap = int((self.default_dimensions[0] - self.rows)/2)
        cols_gap = int((self.default_dimensions[1] - self.cols)/2)

        for i in range(self.rows):
            for j in range(self.cols):
                self.add_widget(self.grid[i + rows_gap][j + cols_gap])

    # upload on board different patterns from patterns folder
    # only 5 have been used on the layout.kv file but all the others can be used as well
    def upload_pattern(self, file="1beacon"):

        if file is not 'Empty':
            x, y, map_string = self.decorder.decode_pattern((file+'.rle'))
            self.clear()

            rows_gap = int(self.default_dimensions[0]/2) - int(x/2)
            cols_gap = int(self.default_dimensions[1]/ 2) - int(y/2)

            # alg to draw uploaded pattern on board
            # decoding following the b3/s23 rule
            i, j = 0, 0  # iterators
            for s in map_string:
                if s == '!': break
                if s == '$':
                    j, i = 0, i + 1
                    continue
                if s == 'o':
                    self.grid[i + rows_gap][j + cols_gap].status = 1
                    self.grid[i + rows_gap][j + cols_gap].background_color = 0, 0, 0, 1
                j += 1
                if j > y:
                    j = 0, i + 1
                    if i == x: break

    # clear the game board
    def clear(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                cell.status = 0
                cell.next_status = 0
                cell.generation = 0
                cell.background_color = 1, 1, 1, 1
        self.step = 0
        Clock.unschedule(self.new_step)

    # function scheduled and unscheduled by the kivy Clock to animate the board
    # make progress for all cells at each new step
    def new_step(self, a):
        for child in self.children: child.progress()
        for child in self.children: child.apply()
        self.step += 1


# -- main application screen -- #
class GameLayout(Screen):
    board = ObjectProperty(None)
    speed = 1

    # start simulation
    def start(self):
        Clock.schedule_interval(self.board.new_step, self.speed)
        for child in self.children:
            child.start.text = "Start"

    # pause simulation
    def pause(self, start=True):
        Clock.unschedule(self.board.new_step)
        if start:
            for child in self.children:
                child.start.text = "Resume"

    def clear(self):
        Clock.unschedule(self.board.new_step)
        self.board.clear()
        for child in self.children:
            child.start.text = "Start"
