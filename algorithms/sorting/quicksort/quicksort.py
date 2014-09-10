"""
quicksort.py -- sorts an array of integers using the Quicksort sorting algorithm. When executed, uses a randomized
version of quicksort to obtain a good average-case performance over all inputs.
"""

__author__ = 'Tom'

import random

class Quicksort(object):
    """
    A class that contains methods that implement the quicksort sorting algorithm.
    """
    def __init__(self, data):
        """ Initializes a new Quicksort object

        Attributes:

            data -- an array of integers
        """
        self.data = data
        
    def sort(self, p, r):
        """ Sorts the elements of self.data from p to r

        Attributes:

            p -- a starting index
            r -- an end index
        """
        if p < r:
            q = self.partition(p, r)
            self.sort(p, q - 1)
            self.sort(q + 1, r)
    
    def partition(self, p, r):
        """ Partitions the subarray self.data[p..r] around a pivot element, self.data[r], moving it into its place in
        the array.

        Attributes:

            p -- a starting index
            r -- an end index
        """
        x = self.data[r]
        i = p - 1
        for j in range(p, r):
            if self.data[j] <= x:
                i += 1
                self.swap(i, j)
        self.swap(i + 1, r)
        return i + 1

    def swap(self, i, j):
        """ Swap elements at i and j
        """
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp
    
    def randomized_sort(self, p, r):
        """ Sorts the elements of self.data from p to r using a randomized partition.
        """
        if p < r:
            q = self.randomized_partition(p, r)
            self.randomized_sort(p, q - 1)
            self.randomized_sort(q + 1, r)
    
    def randomized_partition(self, p, r):
        """ Partitions the subarray self.data[p..r] around a randomly-chosen pivot element.
        """
        i = random.randint(p, r)
        self.swap(r, i)
        return self.partition(p, r)

if __name__ == "__main__":
    import argparse
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Sort integers using quicksort')
    # add arguments
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the sort')
    parser.add_argument('--begin', metavar='P', type=int, default=0, help='an integer for the start index')
    parser.add_argument('--end', metavar='R', type=int, help='an integer for the end index')
    # parse arguments
    args = parser.parse_args()
    # populates end index if it is None
    if args.end is None:
        args.end = len(args.integers) - 1
    # sort the integers
    q = Quicksort(args.integers)
    q.randomized_sort(args.begin, args.end)
    # print the resulting, sorted array
    print q.data