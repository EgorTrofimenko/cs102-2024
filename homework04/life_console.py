import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.addstr(0, 0, "/" + "-" * self.life.cols + "\\")
        screen.addstr(self.life.rows + 1, 0, "\\" + "-" * self.life.cols + "/")

        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, "|")
            screen.addstr(i, self.life.cols + 1, "|")

        screen.addstr(self.life.rows + 2, 0, "Press 'q' to quit")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addch(row + 1, col + 1, "*")
                else:
                    screen.addch(row + 1, col + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.timeout(100)
        running = True
        while running == True:
            screen.clear()

            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()

            if self.life.is_max_generations_exceeded:
                screen.addstr(0, 0, "Max generations exceeded")
                screen.refresh()
            if not self.life.is_changing:
                screen.addstr(0, 0, "Nothing changing")
                screen.refresh()

            key = screen.getch()

            if key == ord("q"):
                running = False
                break
            curses.endwin()


if __name__ == "__main__":
    life_game = GameOfLife((20, 20), max_generations=50)
    ui = Console(life_game)
    ui.run()
