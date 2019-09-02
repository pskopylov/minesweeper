from minesweeper import Minesweeper
import constatnts

if __name__ == "__main__":
    size = (constatnts.ROWS, constatnts.COLS)
    mines = 10
    minesweeper = Minesweeper(size, mines)
    minesweeper.run_game()
