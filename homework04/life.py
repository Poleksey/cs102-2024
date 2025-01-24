import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=True)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        grid = [[0] * self.cols for _ in range(self.rows)]
        if not randomize:
            return grid
        for y in range(self.rows):
            for x in range(self.cols):
                grid[y][x] = random.randint(0, 1)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        cells = []
        y_loc, x_loc = cell[0], cell[1]

        for y in range(y_loc - 1, y_loc + 2):
            for x in range(x_loc - 1, x_loc + 2):
                if (y, x) != cell and 0 <= y < self.rows and 0 <= x < self.cols:
                    cells.append(self.curr_generation[y][x])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        new_grid = [[0] * self.cols for _ in range(self.rows)]
        for y, row in enumerate(self.curr_generation):
            for x, _ in enumerate(row):

                alive_neighbours = sum(self.get_neighbours((y, x)))
                if alive_neighbours in (2, 3) and self.curr_generation[y][x] == 1:
                    new_grid[y][x] = 1
                elif alive_neighbours == 3 and self.curr_generation[y][x] == 0:
                    new_grid[y][x] = 1
                if alive_neighbours > 3:
                    new_grid[y][x] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """

        if self.max_generations is not None and self.generations > self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли   состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as gen_from_file:
            container = gen_from_file.read()

        lines = container.split()
        repo_of_lines: list[list] = []

        for i in range(len(lines)):
            element = list(lines[i])
            repo_of_lines.append(element)
        game = GameOfLife(size=((len(lines)), len(lines[0])))
        game.curr_generation = repo_of_lines
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            steck = []
            for i in self.curr_generation:
                temp_el = "".join(map(str, i))
                steck.append(temp_el)
            for result in steck:
                print(steck[0], file=f, sep="n")
        pass
