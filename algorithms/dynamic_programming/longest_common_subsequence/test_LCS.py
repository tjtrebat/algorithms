from unittest import TestCase
from algorithms.dynamic_programming.longest_common_subsequence.lcs import LCS

__author__ = 'Tom'

class TestLCS(TestCase):
    def test_get_lcs(self):
        x, y = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA", "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
        lcs = LCS(x, y)
        lcs.lcs_length()
        self.assertEqual(lcs.get_lcs(len(x), len(y)), "GTCGTCGGAAGCCGGCCGAA")