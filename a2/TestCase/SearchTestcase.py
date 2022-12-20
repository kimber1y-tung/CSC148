from __future__ import annotations
import unittest
from typing import *
from puzzle import Puzzle
from puzzle_tools import depth_first_solve, breadth_first_solve
class GraphPuzzle(Puzzle):
    map: Dict[int: List[int]]
    cur: int
    to: int
    def __init__(self, i, m, t):
        self.map = m
        self.cur = i
        self.to = t

    def extensions(self) -> List[Puzzle]:
        return [GraphPuzzle(i, self.map, self.to) for i in self.map.get(self.cur, [])]


    def __str__(self):
        return "GraphPuzzle({}, {}, {})".format(str(self.cur), str(self.map), str(self.to))

    def is_solved(self) -> bool:
        return self.cur == self.to

    def __eq__(self, other):
        return self.map == other.map and self.cur == other.cur and self.to == other.to


class TestSolver(unittest.TestCase):
    t1 = {1: [2], 2: [3, 4], 3: [4], 4: [5]}
    t2 = {1: [2]}
    t3 = {1: [2], 2: [3], 3:[1]}

    def test_regualar(self):
        exp = """GraphPuzzle(1, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(2, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(3, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(4, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(5, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

"""
        act = str(depth_first_solve(GraphPuzzle(1, self.t1, 5)))
        self.assertEqual(exp, act, "Your solver doesnt run in the right way")

        exp2 = """GraphPuzzle(1, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(2, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(4, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

GraphPuzzle(5, {1: [2], 2: [3, 4], 3: [4], 4: [5]}, 5)

"""
        act2 = str(breadth_first_solve(GraphPuzzle(1, self.t1, 5)))
        self.assertEqual(exp2, act2, "You should return the shortest path")

    def test_no_solution(self):
        exp = None
        act = depth_first_solve(GraphPuzzle(1, self.t2, 5))
        self.assertEqual(exp, act)

        exp = None
        act = breadth_first_solve(GraphPuzzle(1, self.t2, 5))
        self.assertEqual(exp, act)

    def test_check_seen(self):
        exp = None
        act = depth_first_solve(GraphPuzzle(1, self.t3, 5))
        self.assertEqual(exp, act)

        exp = None
        act = breadth_first_solve(GraphPuzzle(1, self.t3, 5))
        self.assertEqual(exp, act)
if __name__ == "__main__":
    unittest.main()

