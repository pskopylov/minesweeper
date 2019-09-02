class Cell(object):

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__value = 0
        self.__mine = False
        self.__opened = False
        self.__marked = False
        self.__image = None

    def is_mine(self):
        return self.__mine

    def set_mine(self, mine):
        self.__mine = mine

    def set_value(self, value):
        self.__value = value

    def get_value(self, value):
        self.__value = value

    def is_open(self):
        return self.__opened

    def open(self):
        self.__opened = True

    def mark(self):
        self.__marked = True

    def unmark(self):
        self.__marked = False

    def is_marked(self):
        return self.__marked

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def is_empty_cell(self):
        return (self.__value == 0) and (not self.__mine)

    def is_not_opened_empty_cell(self):
        return (not self.__opened) and self.is_empty_cell()

    def __repr__(self):
        return str(self.__mine)

    def __str__(self):
        return str("*" if self.is_mine() else self.__value)
