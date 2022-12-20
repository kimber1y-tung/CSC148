import unittest
from mn_puzzle import MNPuzzle

class TestExtension(unittest.TestCase):

    p1 = (("3", "1", "3"),
          ("4", "5", "*"))

    p2 = (('3', '1', '*'),
          ('4', '5', '3'))
    p3 = (('3', '1', '3'),
          ('4', '*', '5'))

    fs = [p2, p3]

    def test_extension(self):
        ans = {str(MNPuzzle(i, self.p1)) for i in self.fs}
        act = {str(i) for i in MNPuzzle(self.p1, self.p1).extensions()}
        self.assertEqual(ans, act)

    def test_issolved(self):
        ans = True
        act = MNPuzzle(self.p1, self.p1).is_solved()
        self.assertEqual(ans, act)

if __name__ == "__main__":
    unittest.main()
