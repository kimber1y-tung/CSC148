import unittest
from word_ladder_puzzle import WordLadderPuzzle

class WordTest(unittest.TestCase):
    words = {'aaaa', 'aaab', 'aaac', 'aaad', 'aaba', 'aabb', 'aabc', 'aabd', 'aaca', 'aacb', 'aacc', 'aacd', 'aada', 'aadb', 'aadc', 'aadd', 'abaa', 'abab', 'abac', 'abad', 'abba', 'abbb', 'abbc', 'abbd', 'abca', 'abcb', 'abcc', 'abcd', 'abda', 'abdb', 'abdc', 'abdd', 'acaa', 'acab', 'acac', 'acad', 'acba', 'acbb', 'acbc', 'acbd', 'acca', 'accb', 'accc', 'accd', 'acda', 'acdb', 'acdc', 'acdd', 'adaa', 'adab', 'adac', 'adad', 'adba', 'adbb', 'adbc', 'adbd', 'adca', 'adcb', 'adcc', 'adcd', 'adda', 'addb', 'addc', 'addd', 'baaa', 'baab', 'baac', 'baad', 'baba', 'babb', 'babc', 'babd', 'baca', 'bacb', 'bacc', 'bacd', 'bada', 'badb', 'badc', 'badd', 'bbaa', 'bbab', 'bbac', 'bbad', 'bbba', 'bbbb', 'bbbc', 'bbbd', 'bbca', 'bbcb', 'bbcc', 'bbcd', 'bbda', 'bbdb', 'bbdc', 'bbdd', 'bcaa', 'bcab', 'bcac', 'bcad', 'bcba', 'bcbb', 'bcbc', 'bcbd', 'bcca', 'bccb', 'bccc', 'bccd', 'bcda', 'bcdb', 'bcdc', 'bcdd', 'bdaa', 'bdab', 'bdac', 'bdad', 'bdba', 'bdbb', 'bdbc', 'bdbd', 'bdca', 'bdcb', 'bdcc', 'bdcd', 'bdda', 'bddb', 'bddc', 'bddd', 'caaa', 'caab', 'caac', 'caad', 'caba', 'cabb', 'cabc', 'cabd', 'caca', 'cacb', 'cacc', 'cacd', 'cada', 'cadb', 'cadc', 'cadd', 'cbaa', 'cbab', 'cbac', 'cbad', 'cbba', 'cbbb', 'cbbc', 'cbbd', 'cbca', 'cbcb', 'cbcc', 'cbcd', 'cbda', 'cbdb', 'cbdc', 'cbdd', 'ccaa', 'ccab', 'ccac', 'ccad', 'ccba', 'ccbb', 'ccbc', 'ccbd', 'ccca', 'cccb', 'cccc', 'cccd', 'ccda', 'ccdb', 'ccdc', 'ccdd', 'cdaa', 'cdab', 'cdac', 'cdad', 'cdba', 'cdbb', 'cdbc', 'cdbd', 'cdca', 'cdcb', 'cdcc', 'cdcd', 'cdda', 'cddb', 'cddc', 'cddd', 'daaa', 'daab', 'daac', 'daad', 'daba', 'dabb', 'dabc', 'dabd', 'daca', 'dacb', 'dacc', 'dacd', 'dada', 'dadb', 'dadc', 'dadd', 'dbaa', 'dbab', 'dbac', 'dbad', 'dbba', 'dbbb', 'dbbc', 'dbbd', 'dbca', 'dbcb', 'dbcc', 'dbcd', 'dbda', 'dbdb', 'dbdc', 'dbdd', 'dcaa', 'dcab', 'dcac', 'dcad', 'dcba', 'dcbb', 'dcbc', 'dcbd', 'dcca', 'dccb', 'dccc', 'dccd', 'dcda', 'dcdb', 'dcdc', 'dcdd', 'ddaa', 'ddab', 'ddac', 'ddad', 'ddba', 'ddbb', 'ddbc', 'ddbd', 'ddca', 'ddcb', 'ddcc', 'ddcd', 'ddda', 'dddb', 'dddc', 'dddd'}

    def com(self, lst):
        return {str(i) for i in lst}

    def test_extension_regular(self):
        ans1 = [WordLadderPuzzle(a, 'abcd', self.words) for a in self.words if a.count('a') == 3]
        act1 = WordLadderPuzzle('aaaa', 'abcd', self.words).extensions()
        self.assertEqual(self.com(ans1), self.com(act1))

    # def test_extension_regular2(self):
    #     ans1 = [WordLadderPuzzle(a, 'abcd', self.words) for a in self.words if len(self.count_difference(a, 'abcd')) == 1]
    #     act1 = WordLadderPuzzle('abcd', 'abcd', self.words).extensions()
    #     self.assertEqual(self.com(ans1), self.com(act1))
    #
    # def test_extension_no_result(self):
    #     ans1 = []
    #     act1 = WordLadderPuzzle('abcde', 'abcd', self.words).extensions()
    #     self.assertEqual(self.com(ans1), self.com(act1))
    #
    # def count_difference(self, word1, word2):
    #     return [word1[i] for i in range(len(word1)) if word1[i] != word2[i]]


if __name__ == '__main__':
    unittest.main()
