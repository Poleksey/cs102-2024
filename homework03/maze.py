from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    y_loc, x_loc = coord[0], coord[1]
    limit = len(grid[0])
    random_number = randint(0, 1)

    if random_number == 0:
        if y_loc - 2 > 0:
            grid[y_loc - 1][x_loc] = " "
            return grid

        elif x_loc + 2 < limit:
            grid[y_loc][x_loc + 1] = " "
            return grid

    else:
        if x_loc + 2 < limit:
            grid[y_loc][x_loc + 1] = " "
            return grid

        elif y_loc - 2 > 0:
            grid[y_loc - 1][x_loc] = " "
            return grid
    return grid


# def in_out_coord() -> tuple[tuple, tuple]:
# inter = input("Введите координаты начала в целых числах от 0 до 14 через пробел").split()
# outer = input("Введите координаты начала в целых числах от 0 до 14 через пробел").split()
# return (inter, outer)
def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    while empty_cells:
        coord = empty_cells.pop(0)
        remove_wall(grid, coord)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
        # inter_outer =  in_out_coord()
        # y_in, x_in = inter_outer[0]
        # y_out, x_out = inter_outer[1]
    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    in_out = []
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if grid[y][x] == "X":
                in_out.append((y, x))
    # ВОЗВРАЩАЕТ Y ПОТОМ X/ '
    return in_out


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    grid_height, grid_width = len(grid), len(grid[0])
    y, x = coord
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == grid_width - 1)
        or (x == grid_height - 1 and y == 0)
        or (x == grid_height - 1 and y == grid_width - 1)
    ):
        return True

    if x == 0 and grid[y][x + 1] == "■":
        return True
    if x == grid_height - 1 and grid[y][x - 1] == "■":
        return True
    if y == 0 and grid[y + 1][x] == "■":
        return True
    if y == grid_width - 1 and grid[y - 1][x] == "■":
        return True

    return False


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if grid[y][x] == k:
                k += 1
                try:
                    if grid[y + 1][x] == 0:
                        grid[y + 1][x] = k
                except:
                    IndexError
                try:
                    if grid[y][x + 1] == 0:
                        grid[y][x + 1] = k
                except:
                    IndexError

                try:
                    if grid[y][x - 1] == 0 or grid[0][y] == 0:
                        grid[y][x - 1] = k
                except:
                    IndexError
                try:
                    if grid[y - 1][x] == 0:
                        grid[y - 1][x] = k
                except:
                    IndexError
                k -= 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    y, x = exit_coord[0], exit_coord[1]

    temp_k = int(grid[y][x])

    way = [(y, x)]
    while grid[y][x] != 1:
        temp_k -= 1
        if grid[y - 1][x] != "■" and grid[y - 1][x] == temp_k:
            y, x = (y - 1), x
            way.append((y, x))
            continue

        if grid[y][x - 1] != "■" and grid[y][x - 1] == temp_k:
            y, x = (y), (x - 1)
            way.append((y, x))
            continue

        if grid[y + 1][x] != "■" and grid[y + 1][x] == temp_k:
            y, x = (y + 1), x
            way.append((y, x))
            continue
        if grid[y][x + 1] != "■" and grid[y][x + 1] == temp_k:
            y, x = (y), (x + 1)
            way.append((y, x))
            continue
        if len(way) != temp_k:
            delete = way.pop()
            grid[delete[0]][delete[1]] = " "
            y, x = way[0][0], way[0][1]
            continue

    return way


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    # случай с совпадением входа и выхода
    if len(get_exits(grid)) == 1:
        print("Путь есть, и он уже пройден.")
        return grid, get_exits(grid)[0]

    # случай с тупиками
    inter, outer = get_exits(grid)
    if encircled_exit(grid, inter) or encircled_exit(grid, outer):
        print("Нет пути.")
        return grid, None

    grid[inter[0]][inter[1]] = 1
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if grid[y][x] == " " or grid[y][x] == "X":
                grid[y][x] = 0

    k = 0
    while grid[outer[0]][outer[1]] == 0:
        k += 1
        grid = make_step(grid, k)

    way = shortest_path(grid, outer)

    return grid, way


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    # check = str(input("Если хотите ввести координаты, введите Y"))
    # if check == "Y":
    # temp = False
    # else:
    # temp = True
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
