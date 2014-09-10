"""
test_quicksort.py -- tests the quicksort and select modules.
"""
import random
from unittest import TestCase
from algorithms.sorting.quicksort.quicksort import *
from algorithms.sorting.quicksort.select import *

__author__ = 'Tom'

class TestQuicksort(TestCase):
    """ TestQuicksort tests the functions in Quicksort
    """
    def setUp(self):
        """ Sets up each test case
        """
        self.q = Quicksort([2, 8, 7, 1, 3, 5, 6, 4])

    def test_sort(self):
        """ Tests sort
        """
        self.q.sort(0, len(self.q.data) - 1)
        self.assertEqual(self.q.data, sorted(self.q.data))

    def test_randomized_sort(self):
        """ Tests randomized sort
        """
        self.q.randomized_sort(0, len(self.q.data) - 1)
        self.assertEqual(self.q.data, sorted(self.q.data))

class TestSelect(TestCase):
    """ TestSelect tests the functions in Select
    """
    def setUp(self):
        """ Sets up each test case
        """
        self.s = Select([2, 8, 7, 1, 3, 5, 6, 4])

    def test_select(self):
        """ Tests select
        """
        for i in range(len(self.s.data)):
            self.assertEqual(self.s.select(0, len(self.s.data) - 1, i + 1), sorted(self.s.data)[i])

    def test_randomized_select(self):
        """ Tests randomized select
        """
        for i in range(len(self.s.data)):
            self.assertEqual(self.s.randomized_select(0, len(self.s.data) - 1, i + 1), sorted(self.s.data)[i])