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
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """creating a grid"""
        grid = [[0] * self.cols for i in range(self.rows)]

        if randomize:
            for i, row in enumerate(grid):
                for j, _ in enumerate(row):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """finding neighbours"""
        neighbours = []
        row_pos, col_pos = cell
        for i in range(row_pos - 1, row_pos + 2):
            for j in range(col_pos - 1, col_pos + 2):
                if (i, j) != cell and 0 < i < self.rows and 0 < j < self.cols:
                    neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """getting new generation"""
        new_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((i, j)))
                if 2 <= alive_neighbours <= 3 and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 1
                elif alive_neighbours == 3 and self.curr_generation[i][j] == 0:
                    new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
            grid = [[int(cell) for cell in line] for line in lines]

        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = [row for row in grid if row]
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for line in self.curr_generation:
                f.write("".join(map(str, line)) + "\n")
