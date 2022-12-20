"""
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

=== Module Description ===
This module contains the class required to solve grid peg solitaire puzzles.
"""
from __future__ import annotations
from typing import List, Set
from puzzle import Puzzle
import copy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.

    === Public Attributes ===
    None

    === Private Attributes ===
    _marker: the m x n solitaire grid with some pegs, spaces and unused spots
    _marker_set: the possible symbols on the grid, representing different spots

    === Representation Invariants ===
    _marker: a non-empty list of lists representing an m x n grid
    strings in marker are all a valid string from marker_set
    """

    def __init__(self, marker: List[List[str]], marker_set: Set[str]):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        Note: The symbol "#" is for unused, "*" is for peg, "." is for empty

        Precondition:
        - marker is a non-empty list of lists representing an m x n grid
        - the strings in marker are all a valid string from marker_set
        """

        _marker: str
        _marker_set: str

        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation of this
        GridPegSolitairePuzzle.

        >>> r1 = ["*", "*", "*", "*", "*"]
        >>> r2 = ["*", "*", "*", "*", "*"]
        >>> r3 = ["*", "*", ".", "*", "*"]
        >>> r4 = ["*", "*", "*", "*", "*"]
        >>> r5 = ["*", "*", "*", "*", "*"]
        >>> grid = [r1, r2, r3, r4, r5]
        >>> p1 = GridPegSolitairePuzzle(grid, {"*", "#", "."})
        >>> print(p1)
        * * * * *
        * * * * *
        * * . * *
        * * * * *
        * * * * *
        >>> x1 = ["*", "*", "*", "*"]
        >>> x2 = ["*", "*", "*", "*"]
        >>> x3 = ["*", "*", ".", "*"]
        >>> grid = [x1, x2, x3]
        >>> p2 = GridPegSolitairePuzzle(grid, {"*", "#", "."})
        >>> print(p2)
        * * * *
        * * * *
        * * . *
        """
        # "#" is for unused, "*" is for peg, "." is for empty

        m = len(self._marker)
        n = len(self._marker[0])
        ans = ''

        for x in range(m):
            for y in range(n):
                ans += self._marker[x][y]
                if y != (n - 1):
                    ans += ' '
            if x != (m - 1):
                ans += "\n"
        return ans

    def extensions(self) -> List[GridPegSolitairePuzzle]:
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        >>> x1 = ["*", "*", "*", "*", "*"]
        >>> x2 = ["*", "*", "*", "*", "*"]
        >>> x3 = ["*", "*", "*", "*", "*"]
        >>> x4 = ["*", "*", ".", "*", "*"]
        >>> x5 = ["*", "*", "*", "*", "*"]
        >>> grid = [x1, x2, x3, x4, x5]
        >>> x = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> lst = x.extensions()
        >>> len(lst) == 3
        True
        >>> print(lst[0])
        * * * * *
        * * . * *
        * * . * *
        * * * * *
        * * * * *
        >>> print(lst[1])
        * * * * *
        * * * * *
        * * * * *
        . . * * *
        * * * * *
        >>> print(lst[2])
        * * * * *
        * * * * *
        * * * * *
        * * * . .
        * * * * *

        >>> r1 = ["#", "*", "*"]
        >>> r2 = ["*", ".", "*"]
        >>> r3 = ["*", "*", "*"]
        >>> grid = [r1, r2, r3]
        >>> s1 = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> lst2 = s1.extensions()
        >>> print(lst2)
        []
        """

        m = len(self._marker)
        n = len(self._marker[0])

        ans = []

        if self.is_solved():
            return []

        else:
            for x in range(m):
                for y in range(n):

                    if self._marker[x][y] == '*':

                        # up
                        if (x - 2) > 0 and self._marker[x-1][y] == "*" and \
                                self._marker[x-2][y] == ".":
                            temp = copy.deepcopy(self._marker)
                            temp[x][y] = "."
                            temp[x-1][y] = "."
                            temp[x-2][y] = "*"
                            temp = GridPegSolitairePuzzle(temp, self._marker_set)
                            ans.append(temp)

                        # down
                        if (x + 2) < m and self._marker[x + 1][y] == "*" and \
                                self._marker[x + 2][y] == ".":
                            temp = copy.deepcopy(self._marker)
                            temp[x][y] = "."
                            temp[x + 1][y] = "."
                            temp[x + 2][y] = "*"
                            temp = GridPegSolitairePuzzle(temp, self._marker_set)
                            ans.append(temp)

                        # left
                        if (y - 2) > 0 and self._marker[x][y - 1] == "*" and \
                                self._marker[x][y - 2] == ".":
                            temp = copy.deepcopy(self._marker)
                            temp[x][y] = "."
                            temp[x][y - 1] = "."
                            temp[x][y - 2] = "*"
                            temp = GridPegSolitairePuzzle(temp, self._marker_set)
                            ans.append(temp)

                        # right
                        if (y + 2) < n and self._marker[x][y + 1] == "*" and \
                                self._marker[x][y + 2] == ".":
                            temp = copy.deepcopy(self._marker)
                            temp[x][y] = "."
                            temp[x][y + 1] = "."
                            temp[x][y + 2] = "*"
                            temp = GridPegSolitairePuzzle(temp, self._marker_set)
                            ans.append(temp)
            return ans

    def is_solved(self) -> bool:
        """
        Return whether this grid peg solitaire puzzle is solved.

        "*" is for peg, "." is for empty

        >>> r1 = ["*", "*", "*", "*"]
        >>> r2 = ["*", "*", "*", "*"]
        >>> r3 = ["*", "*", ".", "*"]
        >>> r4 = ["*", "*", "*", "*"]
        >>> grid = [r1, r2, r3, r4]
        >>> p1 = GridPegSolitairePuzzle(grid, {"*", "#", "."})
        >>> p1.is_solved()
        False

        >>> x1 = [".", ".", ".", "*"]
        >>> x2 = [".", ".", ".", "."]
        >>> x3 = [".", ".", ".", "."]
        >>> x4 = [".", ".", ".", "."]
        >>> grid = [x1, x2, x3, x4]
        >>> x1 = GridPegSolitairePuzzle(grid, {"*", "#", "."})
        >>> x1.is_solved()
        True
        """

        m = len(self._marker)
        n = len(self._marker[0])
        count = 0

        for x in range(m):
            for y in range(n):
                if self._marker[x][y] == '*':
                    count += 1

        if count == 1:
            # puzzle is solved when there is exactly one "*" left
            return True
        else:
            return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
