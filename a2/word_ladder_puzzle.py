"""
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

=== Module Description ===
This module contains the class required to solve word ladder puzzles.
"""

from __future__ import annotations
from typing import Set, List
from puzzle import Puzzle
import copy


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.

    === Public Attributes ===
    None

    === Private Attributes ===
    _from_word: the initial word the puzzle begins with
    _to_word: the goal word the puzzle wants to change to
    _word_set: the set of all words that are possible valid words to change into
    _chars: a string of all possible characters that a word may consist of

    === Representation Invariants ===
    _from_word and _to_word have the same length
    """

    def __init__(self, from_word: str, to_word: str, ws: Set[str]) -> None:
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.
        """

        _from_word: str
        _to_word: str
        _word_set: Set[str]
        _chars: str

        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        return (type(other) == type(self) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return a human-readable string representation of this WordLadderPuzzle.

        >>> x = {'cast','case'}
        >>> N = WordLadderPuzzle('cost', 'save', x)
        >>> print(N)
        cost -> save
        """
        ans = self._from_word + ' -> ' + self._to_word
        return ans

    def extensions(self) -> List[WordLadderPuzzle]:
        """
        Return list of extensions of WordLadderPuzzle self.

        legal extensions are WordLadderPuzzles that have a from_word that can
        be reached from this one by changing a single letter to one of those
        in self._chars

        >>> x = WordLadderPuzzle('cart', 'bark', {'cart', 'dart', 'cars', 'card', 'bard', 'bark'} )
        >>> for i in x.extensions():
        ...    print(i)
        dart -> bark
        card -> bark
        cars -> bark
        """

        def find_same_length(j: Set, k: str) -> List:
            """
            finds the same length of words in a word set
            """
            h = [*j, ]
            i = []
            for j in h:
                if len(j) == len(k):
                    i.append(j)
            return i

        list_set = find_same_length(self._word_set, self._from_word)
        # list_set is a list of the words in the set with the same length as
        # from_word

        ans = []
        temp_ans = []

        len_word = len(self._from_word)

        for x in range(len_word):
            for y in self._chars:
                temp = copy.deepcopy(self._from_word)
                if temp[x] != y:
                    temp = list(temp)
                    temp[x] = y
                    temp = "".join(temp)
                    temp_ans.append(temp)

        for a in temp_ans:
            for b in list_set:
                if a == b:
                    found = WordLadderPuzzle(a, self._to_word, self._word_set)
                    ans.append(found)
        return ans

    def is_solved(self) -> bool:
        """
        Return whether word ladder puzzle is solved.
        """
        if self._from_word == self._to_word:
            return True
        else:
            return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Comment out the code below as you solve necessary parts of the assignment

    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
