#!/usr/bin/env python

import random
from typing import Tuple, List, Generator, Union, Optional

# The below constants are used to represent the different
# types of cells in the maze.
START_SIGNS = '$Ss'
GOAL_SIGNS = '*Xx'
WALL_SIGNS = '#&;'


class Cell:
    """Cell class represents a cell in the maze.

    Attributes:
        value: The character stored in the cell.
        position: Vertical and horizontal position of the cell in the maze.
        parent: Cell which has been visited before this cell.
        g: Cost from start to this cell.
        h: Estimated cost from this cell to the goal.
        f: Sum of the cost of this cell and the estimated cost to the goal.
    """

    def __init__(self, value: str, position: Tuple[int, int]) -> None:
        self.value = value
        self.position = position
        self.parent = None

        # Default values for g, h and f are same as 0; because this is just a cell
        # and has no brain to calculate the values.
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: 'Cell') -> bool:
        return self.value == other.value and self.position == other.position

    def __str__(self) -> str:
        return f'Cell(value={repr(self.value)}, position={self.position}, parent={self.parent}, g={self.g}, h={self.h}, f={self.f})'

    def __repr__(self) -> str:
        return str(self)


class Maze:
    """The place that represents a 2D grid of cells.

    Attributes:
        grid: A list of cells with their specific position.
        horizontal_limit: The horizontal limit of the maze (x-axis).
        vertical_limit: The vertical limit that we can go (y-axis).
        start: The starting position of the maze.
        goals: The goals positions that we want to reach.
    """

    def __init__(self, maze: str) -> None:
        lines = maze.splitlines()
        rows, cols = len(lines), max(map(len, lines))
        grid = [[Cell(' ', (i, j)) for j in range(cols)] for i in range(rows)]  # Generate a matrix based on the max length of rows
        start = None
        goals = []

        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char not in f'{START_SIGNS}{GOAL_SIGNS}{WALL_SIGNS} ':
                    raise ValueError(f'Invalid character {repr(char)} at position ({i}, {j})')
                elif char in START_SIGNS:
                    if start is not None:
                        raise ValueError('Multiple start positions found!')
                    start = (i, j)
                elif char in GOAL_SIGNS:
                    goals.append((i, j))
                grid[i][j].value = char

        self.grid = grid
        self.horizontal_limit = rows
        self.vertical_limit = cols
        self.start = start
        self.goals = goals

    def __eq__(self, other: 'Maze') -> bool:
        return self.grid == other.grid and self.start == other.start and self.goals == other.goals

    def __str__(self) -> str:
        return f'Maze(grid={self.grid}, horizontal_limit={self.horizontal_limit}, vertical_limit={self.vertical_limit}, start={self.start}, goals={self.goals})'

    def __repr__(self) -> str:
        return str(self)

    def neighbors(self, cell: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
        """Yields all the neighbors that are not walls."""
        current_x, current_y = cell
        coords = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]

        for next_x, next_y in coords:
            x = current_x + next_x
            y = current_y + next_y
            if 0 <= x < self.horizontal_limit and 0 <= y < self.vertical_limit and \
               self.grid[x][y].value not in WALL_SIGNS:
                yield x, y


def _generate_maze(min_size: Tuple[int, int], max_size: Tuple[int, int],
                   save_to_file: Optional[bool] = False) -> Maze:
    """Generates a random maze with the given size."""
    rows, cols = random.randint(*min_size), random.randint(*max_size)
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    # Inserting some walls, starting and goal positions
    for _ in range(random.randint(0, rows*cols//5)):
        grid[random.randint(0, rows-1)][random.randint(0, cols-1)] = '#'
    grid[random.randint(0, rows-1)][random.randint(0, cols-1)] = '$'
    grid[random.randint(0, rows-1)][random.randint(0, cols-1)] = 'X'
    grid = '\n'.join([''.join(row) for row in grid])  # Convert the grid to a string

    if save_to_file:
        with open('genmaze.txt', 'w') as f:
            f.write(grid)
    return Maze(grid)


def _reconstruct_path(current: Cell) -> List[Tuple[int, int]]:
    """Reconstructs the path from the start to the goal."""
    path = [current.position]
    while current.parent is not None:
        current = current.parent
        path.append(current.position)
    return path[::-1]


def _manhattan_distance(current: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def sma_star(maze: Union[Maze, str], bound: Optional[int] = None, forcely: Optional[bool] = False) -> List[Tuple[int, int]]:
    """SMA* searches for the shortest path from the start to the goal(s)."""
    if not isinstance(maze, (Maze, str)):
        raise TypeError('The maze must be a Maze object or a string.')
    elif isinstance(maze, str):
        maze = Maze(maze)

    opened = [maze.grid[maze.start[0]][maze.start[1]]]  # The list initiallized with the starting cell
    closed = []  # No cells have been visited yet

    while opened:
        # print('---------------------------------------------------')
        lowest_f = min(opened, key=lambda cell: cell.f)
        current = opened.pop(opened.index(lowest_f))
        # print(f'Current position is {current.position}')
        closed.append(current)

        if current.position in maze.goals:
            # print(f'Goal found after {len(closed)} steps!')
            print(f'The maximum required bound in this case is {int(bound)}')
            # print('---------------------------------------------------')
            return _reconstruct_path(current)  # Return the path at the first goal found

        for neighbor_x, neighbor_y in maze.neighbors(current.position):
            neighbor_cell = maze.grid[neighbor_x][neighbor_y]
            if neighbor_cell in closed:
                # print(f'Cell {neighbor_cell.position} is already visited')
                continue

            neighbor_cell.parent = current  # Just the current cell as the parent is not good enough, because we need to trace back to the start
            neighbor_cell.g = current.g + 1  # The path cost from the start to the node n increases by 1
            neighbor_cell.h = _manhattan_distance(current.position, neighbor_cell.position)
            neighbor_cell.f = neighbor_cell.g + neighbor_cell.h
            # print(f'Neighbor(position={neighbor_cell.position}, g={neighbor_cell.g}, h={neighbor_cell.h}, f={neighbor_cell.f})')

            if neighbor_cell not in opened:
                opened.append(neighbor_cell)
                # print(f'Cell {neighbor_cell.position} added to the opened list')
            closed.append(neighbor_cell)  # The cell is now visited

        if bound is not None and len(closed) > bound:
            # print(f'The bound of {bound} is reached')
            if not forcely:
                return _reconstruct_path(current)
            bound *= 1.05  # Increase the bound by just 5%

    return None


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Simplified Memory Bounded A* (SMA*) path finding algorithm.')
    parser.add_argument('-m', '--maze', type=str, help='The path to the maze file')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate a new maze and save it to a file')
    parser.add_argument('-b', '--bound', type=int, help='The maximum number of nodes to be expanded')
    parser.add_argument('-f', '--forcely', action='store_true', help='Search the maze even if the bound is reached')
    args = parser.parse_args()

    if args.generate:
        maze = _generate_maze(min_size=(5, 5), max_size=(100, 100), save_to_file=True)
        print('Maze generated!')
    elif args.maze is not None:
        with open(args.maze, 'r') as f:
            maze = Maze(f.read())
        print('Maze loaded!')
    else:
        print('No maze specified! Please read the help for more information.')
        sys.exit(1)

    solution = sma_star(maze, args.bound, args.forcely)
    if solution is None:
        print('No solution found!')
        sys.exit(1)
    print(f'The solution steps in order is: {" -> ".join(map(lambda pos: f"({pos[0]}, {pos[1]})", solution))}\n')

    # Printing the maze with the solution
    for row in maze.grid:
        for cell in row:
            if cell.position in solution[1:-1]:
                cell.value = '∙'
            print(cell.value, end='')
        print()
