"""
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

=== Module Description ===
This module contains the class required to solve mn puzzles.
"""

from __future__ import annotations
from typing import Tuple, List
from puzzle import Puzzle
import copy

class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.

    === Public Attributes ===
    None

    === Private Attributes ===
    _n: the height of the grid
    _m: the width of the grid
    _from_grid: the initial grid arrangement this puzzle begins at
    _to_grid: the goal grid arrangement this puzzle aims to reach

    === Representation Invariants ===
    from_grid and to_grid are rectangular m x n grids

    """

    _n: int
    _m: int
    _from_grid: Tuple
    _to_grid: Tuple

    def __init__(self, from_grid: Tuple, to_grid: Tuple) -> None:
        """
        MNPuzzle in state from_grid, working towards
        state to_grid.

        Note:
            Grid symbols are represented as letters or numerals
            The empty space is represented as a "*"

        Preconditions:
        - both from_grid and to_grid are rectangular m x n grids
        """

        self._n, self._m = len(from_grid), len(from_grid[0])
        self._from_grid, self._to_grid = from_grid, to_grid

    def __eq__(self, other):
        return (type(other) == type(self) and
                self._n == other._n and self._m == other._m and
                self._from_grid == other._from_grid and
                self._to_grid == other._to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of this MNPuzzle.

        >>> target_grid = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*"))
        >>> start_grid = (("1", "4", "5"), ("2", "*", "3"), ("7", "8", "6"))
        >>> mn = MNPuzzle(start_grid, target_grid)
        >>> print(mn)
        1 4 5
        2 * 3
        7 8 6
        -----
        1 2 3
        4 5 6
        7 8 *

        >>> target = (("1", "2", "3"), ("4", "5", "*"))
        >>> start = (("*", "2", "3"), ("1", "4", "5"))
        >>> x = mn = MNPuzzle(start, target)
        >>> print(x)
        * 2 3
        1 4 5
        -----
        1 2 3
        4 5 *
        """
        ans = ''
        separate = '-' * (2 * self._m - 1)

        for x in range(self._n):
            for y in range(self._m):
                ans += self._from_grid[x][y]
                if y != (self._m - 1):
                    ans += ' '
            if x != (self._n - 1):
                ans += "\n"
        ans = ans + "\n" + separate + "\n"

        for x in range(self._n):
            for y in range(self._m):
                ans += self._to_grid[x][y]
                if y != (self._m - 1):
                    ans += ' '
            if x != (self._n - 1):
                ans += "\n"

        return ans

    def extensions(self) -> List[MNPuzzle]:
        """
        legal extensions are configurations that can be reached by swapping one
        symbol to the left, right, above, or below "*" with "*"

        Return list of extensions of MNPuzzle self.

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> lst = x.extensions()
        >>> len(lst)
        2
        """

        def convert(j: List) -> tuple:
            """
            helper function to convert list to tuple
            """
            return tuple(i for i in j)

        temp = [list(row) for row in self._from_grid]
        ans = []

        for x in range(self._n):
            for y in range(self._m):
                if self._from_grid[x][y] == "*":

                    # up
                    if (x - 1) >= 0:
                        temp1 = copy.deepcopy(temp)
                        temp1[x][y], temp1[x - 1][y] = \
                            temp1[x - 1][y], temp1[x][y]
                        temp1 = convert(temp1)
                        temp1 = MNPuzzle(temp1, self._to_grid)
                        ans.append(temp1)

                    # down
                    if (x + 1) < self._n:
                        temp1 = copy.deepcopy(temp)
                        temp1[x][y], temp1[x + 1][y] = \
                            temp1[x + 1][y], temp1[x][y]
                        temp1 = convert(temp1)
                        temp1 = MNPuzzle(temp1, self._to_grid)
                        ans.append(temp1)

                    # left
                    if (y - 1) >= 0:
                        temp1 = copy.deepcopy(temp)
                        temp1[x][y], temp1[x][y - 1] = \
                            temp1[x][y - 1], temp1[x][y]
                        temp1 = convert(temp1)
                        temp1 = MNPuzzle(temp1, self._to_grid)
                        ans.append(temp1)

                    # right
                    if (y + 1) < self._m:
                        temp1 = copy.deepcopy(temp)
                        temp1[x][y], temp1[x][y + 1] = \
                            temp1[x][y + 1], temp1[x][y]
                        temp1 = convert(temp1)
                        temp1 = MNPuzzle(temp1, self._to_grid)
                        ans.append(temp1)
        return ans

    def is_solved(self) -> bool:
        """
        Return whether word ladder puzzle is solved.

        puzzle is solved when from_grid is the same as to_grid
        """
        if self._from_grid == self._to_grid:
            return True
        else:
            return False


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
