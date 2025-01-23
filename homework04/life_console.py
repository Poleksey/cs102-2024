import curses
import pprint

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)
        pass
        # x, y, width, height = 0, 0, self.life.cols+1, self.life.rows+1

        # Рисуем верхнюю и нижнюю линии
        # screen.addch(y, x, "█")
        # screen.addch(y, x + width, "█")
        # screen.addch(y + height, x, "█")
        # screen.addch(y + height, x + width, "█")

        # # Рисуем левую и правую линии
        # for i in range(y + 1, y + height):
        #     screen.addch(i, x, "█")
        #     screen.addch(i, x + width, "█")

        # # Рисуем горизонтальные линии
        # for i in range(x + 1, x + width):
        #     screen.addch(y, i, "█")
        #     screen.addch(y + height, i, "█")

        # screen.refresh()
        # pass

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for y, row in enumerate(self.life.curr_generation):
            for x, el in enumerate(row):
                if el == 1:
                    screen.addch(y + 1, x + 1, "█")
                else:
                    screen.addch(y + 1, x + 1, " ")
        pass

    def run(self) -> None:
        screen = curses.initscr()

        while 0 < 1:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)

            screen.refresh()
            self.life.step()

            if self.life.is_max_generations_exceeded:
                screen.addstr(0, 0, "Достигнут предел поколений. Дальше Бога нет.")
                screen.refresh()
                break

            if self.life.is_changing:
                screen.addstr(0, 0, "Эволюция остановилась.")
                screen.refresh()
                break
            key = screen.getch()

            if key == ord("q"):
                running = False
                break
            # key = screen.getch()
            # if key != curses.ERR:
            # # Если была нажата клавиша, выйти из цикла
            #      break
        curses.endwin()
        pass


life = GameOfLife((24, 80), max_generations=500)
ui = Console(life)
ui.run()
