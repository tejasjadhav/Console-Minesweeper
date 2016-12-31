#!/usr/bin/env python

from __future__ import print_function

import os
from random import randint


class Cell:
    MINE = 'mine'
    FIELD = 'field'

    def __init__(self, cell_type=FIELD):
        self.value = 0
        self.cell_type = cell_type
        self.is_revealed = False

    def increment_value(self):
        self.value += 1

    def __str__(self):
        if not self.is_revealed:
            return '.'

        if self.cell_type == Cell.MINE:
            return  'X'

        if self.value == 0:
            return '-'

        return str(self.value)


class Minesweeper(object):
    ROWS = 10
    COLUMNS = 10
    MINE_COUNT = max(ROWS, COLUMNS)
    CELL_COUNT = ROWS * COLUMNS

    COLORS = (
        '\033[97m',
        '\033[92m',
        '\033[93m',
        '\033[94m',
        '\033[95m',
        '\033[96m',
        '\033[93m',
        '\033[94m',
        '\033[95m',
    )

    BOLD_FORMAT = '\033[1m'

    MINE_COLOR = '\033[101m'
    END_COLOR = '\033[0m'
    RED_COLOR = '\033[41m'
    GREEN_COLOR = '\033[42m'

    def __init__(self):
        self.revealed_cell_count = 0
        self.mine_field = [[Cell() for y in range(self.COLUMNS)] for x in range(self.ROWS)]
        self.mine_count = self.MINE_COUNT

        self.has_game_ended = False
        self.has_won = False

        while self.mine_count:
            x, y = randint(0, self.ROWS - 1), randint(0, self.COLUMNS - 1)

            if self.mine_field[x][y].cell_type == Cell.FIELD:
                self.mine_field[x][y].cell_type = Cell.MINE
                self.mine_count -= 1

                for i in range(3):
                    x_offset = x + i - 1

                    if x_offset < 0 or x_offset > self.ROWS - 1:
                        continue

                    for j in range(3):
                        y_offset = y + j - 1

                        if y_offset < 0 or y_offset > self.COLUMNS - 1:
                            continue

                        cell = self.mine_field[x_offset][y_offset]
                        if cell.cell_type == Cell.FIELD:
                            cell.increment_value()

    def show_minefield(self, reveal=False):
        def tabbed_space(c):
            tab_width = len(str(self.COLUMNS)) + 1
            return ' ' * (tab_width - len(str(c)))

        print(' ' + tabbed_space(' ') + ''.join([tabbed_space(str(j + 1)) + str(j + 1)
                                                 for j in range(self.COLUMNS)]))

        for i, row in enumerate(self.mine_field):
            row_cells = tabbed_space(i + 1) + str(i + 1)

            for cell in row:
                if reveal:
                    cell.is_revealed = True

                row_cells += tabbed_space(cell)

                if not cell.is_revealed:
                    row_cells += str(cell)
                elif cell.cell_type == Cell.MINE:
                    row_cells += self.BOLD_FORMAT + self.MINE_COLOR + str(cell) + self.END_COLOR
                elif cell.cell_type == Cell.FIELD:
                    row_cells += (self.BOLD_FORMAT + self.COLORS[cell.value] + str(cell) +
                                  self.END_COLOR)
                else:
                    row_cells += str(cell)

                if reveal:
                    cell.is_revealed = False

            print(row_cells)

    def explore_cells(self, mine_field, x, y):
        if mine_field[x][y].cell_type != Cell.FIELD or mine_field[x][y].value != 0:
            return

        for i in (-1, 0, 1):
            x_offset = x + i

            if x_offset < 0 or x_offset > self.ROWS - 1:
                continue

            for j in (-1, 0, 1):
                if i == j:
                    continue

                y_offset = y + j

                if y_offset < 0 or y_offset > self.COLUMNS - 1:
                    continue

                cell = mine_field[x_offset][y_offset]
                if not cell.is_revealed:
                    cell.is_revealed = True
                    self.revealed_cell_count += 1
                    self.explore_cells(self.mine_field, x_offset, y_offset)

    def open_cell(self, mine_field, x, y):
        if x > self.ROWS or x < 1 or y > self.COLUMNS or y < 1:
            return

        cell = mine_field[x - 1][y - 1]

        if cell.cell_type == Cell.MINE:
            self.has_game_ended = True
            self.has_won = False
            return

        if cell.cell_type == Cell.FIELD and not cell.is_revealed:
            cell.is_revealed = True
            self.revealed_cell_count += 1
            if cell.value == 0:
                self.explore_cells(self.mine_field, x - 1, y - 1)


    def run(self):
        while not self.has_game_ended:
            os.system('clear')
            self.show_minefield()
            print()
            print('Revealed: %d' % self.revealed_cell_count)
            x, y = map(int, input('Enter x, y: ').split())
            self.open_cell(self.mine_field, x, y)


            if self.revealed_cell_count == (self.CELL_COUNT - self.MINE_COUNT):
                self.has_game_ended = True
                self.has_won = True

        os.system('clear')
        self.show_minefield(True)

        if self.has_won:
            print(self.BOLD_FORMAT + self.GREEN_COLOR + 'You win' + self.END_COLOR)
        else:
            print(self.BOLD_FORMAT + self.RED_COLOR + 'You lose' + self.END_COLOR)

if __name__ == '__main__':
    game = Minesweeper()
    game.run()
