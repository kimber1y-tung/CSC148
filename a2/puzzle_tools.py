"""
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

=== Module Description ===
This module contains the functions that find solutions to puzzles, step by step.
"""

from __future__ import annotations
from typing import List, Optional, Union, Any
from puzzle import Puzzle

# importing a Queue class to possibly use for breadth_first_solve
from collections import deque

# set higher recursion limit
# which is needed in PuzzleNode.__str__
import sys
sys.setrecursionlimit(10**6)

seen = set()
seen2 = set()


def depth_first_solve(puzzle: Puzzle) -> PuzzleNode:
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    idea website:
    https://stackoverflow.com/questions/43430309/depth-first-search-dfs-code-in-python
    """
    # base case
    if puzzle.is_solved():
        return PuzzleNode(puzzle, None)

    curr = PuzzleNode(puzzle, None)

    for x in puzzle.extensions():  # puzzle.extensions() is a list
        if x.__str__() in seen:
            continue
        else:
            seen.add(x.__str__())
            next = depth_first_solve(x)
            if next is not None:
                curr.parent = x
                curr.children.append(next)
                return curr
    return None


def breadth_first_solve(puzzle: Puzzle) -> PuzzleNode:
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    idea website:
    https://www.itread01.com/content/1542363063.html
    """
    # base case
    if puzzle.is_solved():
        return PuzzleNode(puzzle, None)

    curr = PuzzleNode(puzzle, None)
    q = deque()
    q.append(curr)

    found = False
    while len(q) != 0:
        x = q.popleft()
        if x.__str__() in seen2:
            continue
        else:
            seen2.add(x.__str__())
            if x.puzzle.is_solved():
                found = True
                break
            for i in x.puzzle.extensions():
                q.append(PuzzleNode(i, None, x))

    if not found:  # the puzzle is unsolvable
        return None
    else:
        ans = None
        while x:
            ans = PuzzleNode(x.puzzle, children=[ans], parent=None)
            if not ans.children[0] is None:
                ans.children[0].parent = ans
            else:
                ans.children = []
            x = x.parent
        return ans


# The following class has been completed for you
# Do NOT change anything provided in the class below
class PuzzleNode:
    """
    The class PuzzleNode helps build trees of PuzzleNodes that have
    an arbitrary number of children, and a parent.

    === Attributes ===
    puzzle: Optional[Puzzle]
        The configuration (layout) of this puzzle
    children: List[PuzzleNode]
        A list of puzzle nodes that contain puzzles which are extensions (one
        step away) from this puzzle
    parent: Optional[PuzzleNode]
        An optional puzzle node containing a puzzle for which this node's
        puzzle is an extension (one step away) from
    """
    puzzle: Optional[Puzzle]
    children: List[PuzzleNode]
    parent: Optional[PuzzleNode]

    def __init__(self, puzzle: Optional[Puzzle] = None, \
                 children: Optional[List[PuzzleNode]] = None, \
                 parent: Optional[PuzzleNode] = None) -> None:
        """
        Create a new puzzle node self with configuration <puzzle>,
        <children> and <parent>.
        """

        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other: Union[PuzzleNode, Any]) -> bool:
        """
        Return whether this PuzzleNode is equivalent to <other>.

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """

        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self) -> str:
        """
        Return a human-readable string representing PuzzleNode self.
        """

        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
