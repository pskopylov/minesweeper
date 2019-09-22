from minesweeper import Minesweeper
import constants

if __name__ == "__main__":
    size = (constants.ROWS, constants.COLS)
    mines = constants.MINES
    minesweeper = Minesweeper(size, mines)
    minesweeper.run_game()
