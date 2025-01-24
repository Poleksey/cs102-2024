import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    """
    Графический компонент игры
    """

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * 10
        self.height = self.life.rows * 10

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.is_game_paused = False

    def draw_lines(self) -> None:
        """Отобразить линии сетки."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        """Отобразить значения на поле игры."""
        for y, row in enumerate(self.life.curr_generation):
            for x, el in enumerate(row):
                if el == 1:
                    color = pygame.Color("orange")
                else:
                    color = pygame.Color("white")
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
        pass

    def run(self) -> None:
        """
        Функция, приводящая в работу компоненты графики.
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # При нажатии на пробел изменяется состояние игры
                    if event.key == pygame.K_SPACE:
                        self.is_game_paused = not self.is_game_paused

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.is_game_paused:
                        y_loc = mouse_pos[0] // self.cell_size
                        x_loc = mouse_pos[1] // self.cell_size
                        self.life.curr_generation[y_loc][x_loc] = 1 - self.life.curr_generation[y_loc][x_loc]

            # Отрисовка списка клеток
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            if not self.is_game_paused:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        pass


game = GameOfLife((100, 100), True, 400)
gui = GUI(game)
gui.run()
