from unittest import TestCase
from algorithms.dynamic_programming.optimal_bst.optimal_bst import *

__author__ = 'Tom'

class TestOptimalBST(TestCase):
    def setUp(self):
        self.optimal_bst = OptimalBST((.15, .1, .05, .1, .2,), (.05, .1, .05, .05, .05, .1,))
        self.cost = 2.75

    def test_optimal_bst(self):
        n = len(self.optimal_bst.p)
        self.assertEquals(self.optimal_bst.optimal_bst(n)[(0, n - 1)], self.cost)

    def test_optimal_bst_recursive(self):
        n = len(self.optimal_bst.p)
        self.assertEquals(self.optimal_bst.optimal_bst_recursive(n)[(0, n - 1)], self.cost)