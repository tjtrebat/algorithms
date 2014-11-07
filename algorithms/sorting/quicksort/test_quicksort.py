"""
test_quicksort.py -- tests the quicksort and select modules.
"""
import random
from unittest import TestCase
from algorithms.sorting.quicksort import quicksort, select

__author__ = 'Tom'

class TestQuicksort(TestCase):
    """ TestQuicksort tests the functions in Quicksort
    """
    def setUp(self):
        """ Sets up each test case
        """
        self.data = [2, 8, 7, 1, 3, 5, 6, 4]

    def test_sort(self):
        """ Tests sort
        """
        self.assertEqual(sorted(self.data),
            quicksort.sort(self.data, 0, len(self.data) - 1))

    def test_randomized_sort(self):
        """ Tests randomized sort
        """
        self.assertEqual(sorted(self.data),
            quicksort.randomized_sort(self.data, 0, len(self.data) - 1))

class TestSelect(TestCase):
    """ TestSelect tests the functions in Select
    """
    def setUp(self):
        """ Sets up each test case
        """
        self.data = [2, 8, 7, 1, 3, 5, 6, 4]

    def test_select(self):
        """ Tests select
        """
        for i in range(len(self.data)):
            self.assertEqual(sorted(self.data)[i],
                select.select(self.data, 0, len(self.data) - 1, i + 1))

    def test_randomized_select(self):
        """ Tests randomized select
        """
        for i in range(len(self.data)):
            self.assertEqual(sorted(self.data)[i],
                select.randomized_select(self.data, 0, len(self.data) - 1, i + 1))