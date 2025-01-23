import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 1500) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height

        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = copy.copy(self.get_next_generation())

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = True) -> Grid:
        """

        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if not randomize:
            return grid
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                grid[y][x] = random.randint(0, 1)

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        for y, row in enumerate(self.grid):
            for x, el in enumerate(row):
                if el == 1:
                    color = pygame.Color("orange")
                else:
                    color = pygame.Color("white")
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)


    def get_neighbours(self, cell: Cell) -> Cells:
        """

        out : Cells
            Список соседних клеток.
        """
        cells = []
        y_loc, x_loc = cell[0], cell[1]

        try:
            for y in range(y_loc - 1, y_loc + 2):
                for x in range(x_loc - 1, x_loc + 2):
                    if (y, x) != cell and 0 <= y < self.height and 0 <= x < self.width:
                        cells.append(self.grid[y][x])
        except:
            IndexError
        return cells

    def get_next_generation(self) -> Grid:
        """
        out : Grid
           Новое поколение клеток.
        """
        new_grid = self.create_grid(False)

        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                alive_neighbours = sum(self.get_neighbours((y, x)))
                if alive_neighbours in (2, 3) and self.grid[y][x] == 1:
                    new_grid[y][x] = 1
                elif alive_neighbours == 3 and self.grid[y][x] == 0:
                    new_grid[y][x] = 1
                if alive_neighbours > 3:
                    new_grid[y][x] = 0
        return new_grid


game = GameOfLife(1000, 1000, 40)
game.run()
