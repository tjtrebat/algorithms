"""
quicksort.py -- sorts an array of integers using the Quicksort sorting algorithm. When executed, uses a randomized
version of quicksort to obtain a good average-case performance over all inputs.
"""

__author__ = 'Tom'

import random
        
def sort(data, p, r):
    """ Sorts the data from p to r

    Attributes:

        data -- an array of elements
        p -- a starting index
        r -- an end index
    """
    if p < r:
        q = partition(data, p, r)
        sort(data, p, q - 1)
        sort(data, q + 1, r)
    return data

def partition(data, p, r):
    """ Partitions the subarray data[p..r] around a pivot element, data[r], moving it into its place in
    the array.

    Attributes:

        data -- an array of elements
        p -- a starting index
        r -- an end index
    """
    x = data[r]
    i = p - 1
    for j in range(p, r):
        if data[j] <= x:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[r] = data[r], data[i + 1]
    return i + 1

def randomized_sort(data, p, r):
    """ Sorts the data from p to r using a randomized partition.
    """
    if p < r:
        q = randomized_partition(data, p, r)
        randomized_sort(data, p, q - 1)
        randomized_sort(data, q + 1, r)
    return data

def randomized_partition(data, p, r):
    """ Partitions the subarray data[p..r] around a randomly-chosen pivot element.
    """
    i = random.randint(p, r)
    data[r], data[i] = data[i], data[r]
    return partition(data, p, r)

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
    # print sorted array
    print randomized_sort(args.integers, args.begin, args.end)