"""
select.py -- selects the ith smallest element from an array of integers. When executed, uses the median of medians
algorithm to find a pivot that is guaranteed to be within the 30th and 70th percentiles.
"""

__author__ = 'Tom'

import quicksort

class Select(quicksort.Quicksort):
    """
    A class that contains methods that implement a quickselect selection algorithm.
    """
    def __init__(self, data):
        super(Select, self).__init__(data)

    def select(self, p, r, i):
        """ Selects the ith smallest elements of self.data from p to r. Guarantees a good split by choosing the median
        of medians of blocks of size 5.

        Attributes:

            p -- a starting index
            r -- an end index
            i -- an index of the smallest element
        """
        if p == r:
            return self.data[p]
        # divide the group of elements into n/5 groups of 5 elements each
        medians = [] # a list of medians from each group
        last = r
        for j in range(p, last + 1, 4):
            end = j + 5
            if end > last + 1:
                end = last + 1
            self.insertion_sort(j, end)
            mid = (j + end - 1) / 2
            medians.append(self.data.pop(mid))
            last -= 1
        # put medians at the head of the list
        self.data[p:p] = medians
        # use select recursively to find the median of medians
        median = self.select(p, p + len(medians) - 1, (len(medians) + 1) / 2)
        self.swap(self.data.index(median), r)
        q = self.partition(p, r)
        k = q - p + 1
        if i == k:
            return self.data[q]
        elif i < k:
            return self.select(p, q - 1, i)
        else:
            return self.select(q + 1, r, i - k)

    def insertion_sort(self, p, r):
        """ Sorts the elements of self.data from p to r """
        for j in range(1, r):
            key = self.data[j]
            # insert data[j] into the sorted sequence data[p:j-1]
            i = j - 1
            while i > p - 1 and self.data[i] > key:
                self.data[i + 1] = self.data[i]
                i -= 1
            self.data[i + 1] = key

    def randomized_select(self, p, r, i):
        """ Selects the ith smallest elements of self.data from p to r.
        """
        if p == r:
            return self.data[p]
        q = self.randomized_partition(p, r)
        k = q - p + 1
        if i == k: # pivot value is the answer
            return self.data[q]
        elif i < k:
            return self.randomized_select(p, q - 1, i)
        else:
            return self.randomized_select(q + 1, r, i - k)

if __name__ == "__main__":
    import argparse
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Select the ith smallest integer')
    # add arguments
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the selection')
    parser.add_argument('--select', metavar='I', type=int, default=1, help='an integer for the ith smallest element')
    parser.add_argument('--begin', metavar='P', type=int, default=0, help='an integer for the start index')
    parser.add_argument('--end', metavar='R', type=int, help='an integer for the end index')
    # parse arguments
    args = parser.parse_args()
    # populates end index if it is None
    if args.end is None:
        args.end = len(args.integers) - 1
    # print the ith smallest element
    s = Select(args.integers)
    print s.select(args.begin, args.end, args.select)
