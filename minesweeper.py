#!/usr/bin/env python

import os

from random import randint

FIELD = 'field'
MINE = 'mine'

ROWS = 10
COLUMNS = 10
MINE_COUNT = max(ROWS, COLUMNS)
CELL_COUNT = ROWS * COLUMNS

revealed_cell_count = 0

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
GREEN_COLOR =  '\033[42m'

GAME_END = False
WIN = False

def show_minefield(mine_field, reveal=False):
    def tabbed_space(c):
        tab_width = len(str(COLUMNS)) + 1
        return ' ' * (tab_width - len(str(c)))

    print ' ' + tabbed_space(' ') + ''.join([tabbed_space(str(j + 1)) + str(j + 1) for j in range(COLUMNS)])

    for i, row in enumerate(mine_field):
        row_cells = tabbed_space(i + 1) + str(i + 1)
        
        for cell in row:
            if reveal:
                cell.reveal(True)
            
            row_cells += tabbed_space(cell)
            
            if not cell.is_revealed():
                row_cells += str(cell)
            elif cell.get_cell_type() == MINE:
                row_cells += BOLD_FORMAT + MINE_COLOR + str(cell) + END_COLOR
            elif cell.get_cell_type() == FIELD:
                row_cells += BOLD_FORMAT + COLORS[cell.get_value()] + str(cell) + END_COLOR
            else:
                row_cells += str(cell)

            if reveal:
                cell.reveal(False)

        print row_cells

def explore_cells(mine_field, x, y):
    global revealed_cell_count
    
    if mine_field[x][y].get_cell_type() != FIELD or mine_field[x][y].get_value() != 0:
        return

    for i in (-1, 0, 1):
        x_offset = x + i

        if x_offset < 0 or x_offset > ROWS - 1:
            continue

        for j in (-1, 0, 1):
            if i == j:
                continue

            y_offset = y + j

            if y_offset < 0 or y_offset > COLUMNS - 1:
                continue
            
            cell = mine_field[x_offset][y_offset]
            if not cell.is_revealed():
                cell.reveal(True)
                revealed_cell_count += 1
                explore_cells(mine_field, x_offset, y_offset)

def open_cell(mine_field, x, y):
    global revealed_cell_count
    global GAME_END
    global WIN

    if x > ROWS or x < 1 or y > COLUMNS or y < 1:
        return

    cell = mine_field[x - 1][y - 1]

    if cell.get_cell_type() == MINE:
        GAME_END = True
        WIN = False
        return
    
    if cell.get_cell_type() == FIELD and not cell.is_revealed():
        cell.reveal(True)
        revealed_cell_count += 1
        if cell.get_value() == 0:
            explore_cells(mine_field, x - 1, y - 1)

class Cell:
    def __init__(self, cell_type=FIELD):
        self.value = 0
        self.cell_type = cell_type
        self.revealed = False

    def increment_value(self):
        self.value += 1

    def get_value(self):
        return self.value

    def is_revealed(self):
        return self.revealed
    
    def reveal(self, reveal):
        self.revealed = reveal

    def set_cell_type(self, cell_type):
        self.cell_type = cell_type
    
    def get_cell_type(self):
        return self.cell_type
    
    def __str__(self):
        if not self.revealed:
            return '.'
        
        if self.cell_type == MINE:
            return  'X'
        
        if self.value == 0:
            return '-'

        return str(self.value)

mine_field = [[Cell() for y in range(COLUMNS)] for x in range(ROWS)]

mine_count = MINE_COUNT

while mine_count:
    x, y = randint(0, ROWS - 1), randint(0, COLUMNS - 1)

    if mine_field[x][y].get_cell_type() == FIELD:
        mine_field[x][y].set_cell_type(MINE)
        mine_count -= 1
        
        for i in range(3):
            x_offset = x + i - 1
            
            if x_offset < 0 or x_offset > ROWS - 1:
                continue
            
            for j in range(3):
                y_offset = y + j - 1

                if y_offset < 0 or y_offset > COLUMNS - 1:
                    continue
                
                cell = mine_field[x_offset][y_offset]
                if cell.get_cell_type() == FIELD:
                    cell.increment_value()


while not GAME_END:
    os.system('clear')
    show_minefield(mine_field)
    print
    print 'Revealed: %d' % revealed_cell_count
    x, y = map(int, raw_input('Enter x, y: ').split())
    open_cell(mine_field, x, y)
    

    if revealed_cell_count == (CELL_COUNT - MINE_COUNT):
        GAME_END = True
        WIN = True

os.system('clear')
show_minefield(mine_field, True)

if WIN:
    print BOLD_FORMAT + GREEN_COLOR + 'You win' + END_COLOR
else:
    print BOLD_FORMAT + RED_COLOR + 'You lose' + END_COLOR
