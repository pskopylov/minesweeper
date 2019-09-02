import random
import constatnts
from mapper import NUM_MAP
from cell import Cell


class Field(object):

    def __init__(self, h, w, num_of_mines):
        self.h = h
        self.w = w
        self.num_of_mines = num_of_mines
        self.cells = []
        self.opened_cells = 0
        self.__create_cells()

    def __create_cells(self):
        for x in range(self.w):
            self.cells.append([])
            for y in range(self.h):
                self.cells[x].append(None)
        self.__fill_mines()
        self.__fill_cells()

    def __fill_mines(self):
        mines_coordinates = []
        for _ in range(self.num_of_mines):
            while 1:
                x, y = random.randrange(0, self.w), random.randrange(0, self.h)
                if (x, y) not in mines_coordinates:
                    mines_coordinates.append((x, y))
                    cell = Cell(x, y)
                    cell.set_mine(True)
                    cell.set_image(constatnts.MINE_IMAGE)
                    self.cells[x][y] = cell
                    break

    def __fill_cells(self):
        for x in range(self.w):
            for y in range(self.h):
                if self.cells[x][y] is None:
                    self.cells[x][y] = self.__calculate_cell(x, y)

    def __calculate_cell(self, x, y):
        new_cell = Cell(x, y)
        value = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_x = x - i
                new_y = y - j
                if (0 <= new_x < self.w) and (0 <= new_y < self.h):
                    cell = self.cells[new_x][new_y]
                    if (cell is not None) and cell.is_mine():
                        value += 1
        image = NUM_MAP.get(value)
        new_cell.set_image(image)
        new_cell.set_value(value)
        return new_cell

    def open_cells(self, x, y):
        cell = self.cells[x][y]
        self.__open_cell(cell)
        if cell.is_empty_cell():
            self.__open_empty_cells(x, y)
        elif cell.is_mine():
            cell.set_image(constatnts.RED_MINE_IMAGE)
            self.__open_mines()

    def __open_mines(self):
        for rows in self.cells:
            for cell in rows:
                if cell.is_mine():
                    self.__open_cell(cell)

    def __open_empty_cells(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i + j) == 1:
                    new_x = x - i
                    new_y = y - j
                    if (0 <= new_x < self.w) and (0 <= new_y < self.h):
                        cell = self.cells[new_x][new_y]
                        if cell.is_not_opened_empty_cell():
                            self.open_cells(new_x, new_y)
                        elif not (cell.is_mine() or cell.is_open()):
                            self.__open_cell(cell)

    def __open_cell(self, cell):
        self.opened_cells += 1
        cell.open()

    def mark_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_marked():
            cell.unmark()
        else:
            cell.mark()

    def __check_marked(self):
        count = 0
        for rows in self.cells:
            for cell in rows:
                if cell.is_marked() and cell.is_mine():
                    count += 1
        return count == self.num_of_mines

    def get_cells(self):
        return self.cells

    def check_win(self):
        return self.w * self.h - self.num_of_mines == self.opened_cells or self.__check_marked()

    def __repr__(self):
        field = ""
        for x in range(self.w):
            row = ""
            for y in range(self.h):
                row += str(self.cells[x][y])
            field += row + "\n"
        return field
