import unittest
from sudoku_puzzle import SudokuPuzzle

class TestFailFasr(unittest.TestCase):

    l1 = [["1", "2", "3", "4"],
          ["1", "2", "3", "4"],
          ["1", "2", "3", "4"],
          ["1", "2", "3", "4"]]

    l2 = [["1", "2", "3", "4"],
          ["3", "4", "1", "2"],
          ["2", "3", "4", "1"],
          ["4", "1", "2", "3"]]

    l3 = [["1", "2", "3", "*"],
          ["2", "3", "*", "*"],
          ["*", "*", "*", "*"],
          ["*", "*", "*", "*"]
          ]

    l4 = [["*", "*", "*", "*"],
          ["*", "*", "*", "*"],
          ["*", "*", "*", "*"],
          ["*", "*", "*", "*"]
          ]
    symbol_set = set(["1", "2", "3", "4"])

    def test_fail_fast(self):
        p1 = SudokuPuzzle(4, self.l1, self.symbol_set)
        p2 = SudokuPuzzle(4, self.l2, self.symbol_set)
        p3 = SudokuPuzzle(4, self.l3, self.symbol_set)
        p4 = SudokuPuzzle(4, self.l4, self.symbol_set)
        self.assertEqual(p1.fail_fast(), True, "You should return false for puzzles that are unsolveable.")
        self.assertEqual(p2.fail_fast(), False, "You should return true for puzzles that are solved")
        self.assertEqual(p3.fail_fast(), True)
        self.assertEqual(p4.fail_fast(), False)

