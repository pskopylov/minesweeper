import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from field import Field
import constatnts


class Minesweeper(object):

    def __init__(self, size, mines):
        self.__rows = size[0]
        self.__cols = size[1]
        self.__mines = mines
        self.__cell_size = constatnts.CELL_SIZE
        self.__win = False
        self.__game_over = False
        self.__mark = False
        self.__field = Field(self.__rows, self.__cols, self.__mines)

    def run_game(self):
        self.__init_frame()

    def __draw(self, canvas):
        for x in range(self.__rows):
            for y in range(self.__cols):
                cell = self.__field.get_cells()[x][y]
                self.__draw_cell(canvas, cell)
        self.__check_is_over(canvas)
        self.__draw_bottom(canvas)

    # noinspection PyMethodMayBeStatic
    def __draw_bottom(self, canvas):
        p1 = (0, self.__cols * self.__cell_size)
        p2 = (self.__rows * self.__cell_size, self.__cols * self.__cell_size)
        canvas.draw_line(p1, p2, constatnts.LINE_WIDTH, constatnts.LINE_COLOR)
        canvas.draw_text("Mark mode: " + str(self.__mark), (5, self.__rows * self.__cell_size + 15),
                         constatnts.MARK_MODE_TEXT_SIZE, constatnts.FONT_COLOR)

    def __draw_image(self, canvas, cell, is_block, is_mark):
        image = cell.get_image()
        if is_block:
            image = constatnts.BLOCK_IMAGE
        elif is_mark:
            image = constatnts.FLAG_IMAGE
        canvas.draw_image(image, constatnts.BLOCK_CENTER, constatnts.BLOCK_SIZE,
                          (self.__cell_size * (cell.get_x() + 0.5), self.__cell_size * (cell.get_y() + 0.5)),
                          (self.__cell_size, self.__cell_size))

    def __draw_cell(self, canvas, cell):
        if cell.is_open():
            self.__draw_opened_cell(canvas, cell)
        elif cell.is_marked():
            self.__draw_marked_cell(canvas, cell)
        else:
            self.__draw_image(canvas, cell, True, False)

    def __draw_marked_cell(self, canvas, cell):
        self.__draw_image(canvas, cell, False, True)

    def __draw_opened_cell(self, canvas, cell):
        if cell.is_mine():
            self.__draw_mine(canvas, cell)
        else:
            self.__draw_image(canvas, cell, False, False)

    def __draw_mine(self, canvas, cell):
        self.__draw_image(canvas, cell, False, False)
        self.__game_over = False if self.__win else True

    def __check_is_over(self, canvas):
        if self.__game_over:
            self.__game_over_result(canvas)
        elif self.__field.check_win():
            self.__win_result(canvas)

    # noinspection PyMethodMayBeStatic
    def __game_over_result(self, canvas):
        canvas.draw_text(constatnts.GAME_OVER_TEXT, (30, constatnts.HEIGHT - 10),
                         constatnts.RESULT_FONT_SIZE, constatnts.GAME_OVER_COLOR)

    def __win_result(self, canvas):
        self.__mark_all_mines(canvas)
        canvas.draw_text(constatnts.WIN_TEXT, (50, constatnts.HEIGHT - 10),
                         constatnts.RESULT_FONT_SIZE, constatnts.WIN_COLOR)
        self.__win = True

    def __mark_all_mines(self, canvas):
        for x in range(self.__rows):
            for y in range(self.__cols):
                cell = self.__field.get_cells()[x][y]
                if cell.is_mine():
                    self.__draw_image(canvas, cell, False, True)

    def __click(self, pos):
        if not (self.__game_over or self.__win):
            x = int(pos[0] // self.__cell_size)
            y = int(pos[1] // self.__cell_size)
            if y < self.__cols:
                if self.__mark:
                    self.__field.mark_cell(x, y)
                else:
                    self.__field.open_cells(x, y)

    def __restart_button_handler(self):
        self.__game_over = False
        self.__win = False
        self.__mark = False
        self.__field = Field(self.__rows, self.__cols, self.__mines)

    def __mark_button_handler(self):
        self.__mark = False if self.__mark else True

    def __init_frame(self):
        frame = simplegui.create_frame("Minesweeper", constatnts.WIDTH, constatnts.HEIGHT)
        frame.set_canvas_background(constatnts.BG_COLOR)
        frame.set_draw_handler(self.__draw)
        frame.set_mouseclick_handler(self.__click)
        frame.add_button("Restart", self.__restart_button_handler)
        frame.add_button("Mark mines", self.__mark_button_handler)
        frame.start()
