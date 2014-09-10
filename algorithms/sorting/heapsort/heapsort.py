"""
heapsort.py -- A heapsort sorting algorithm.
"""

__author__ = 'Tom'

import math

class Node(object):
    def __init__(self, value, key=None):
        self.value = value
        self.key = key
        self.parent = None

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __repr__(self):
        return str(self.value)

class Heap(object):
    """
    A binary heap object that can be used as either a min or max heap.
    """
    def __init__(self, data):
        """
        Constructs a new Heap object from collection of elements
        and comparator function that allows you to specify
        how elements are compared to each other to satisfy the
        min or max heap property. Defaults to a max heap.

        Attributes:
            data -- input data in the heap array
            comparator -- function used to compared to heap elements
        """
        self.data = data
        self.heap_size = len(data)
        self.comparator = lambda x, y: x > y
        self.default_key = float("-inf") # default key value for max_heap_insert

    def max_heapify(self, i):
        """
        max_heapify is called on an element at index i to let the element "float down" in the heap so that the subtree
        rooted at index i becomes a max-heap.
        """
        left = self.left_child(i)
        right = self.right_child(i)
        if left <= self.heap_size - 1 and self.comparator(self.data[left], self.data[i]):
            largest = left
        else:
            largest = i
        if right <= self.heap_size - 1 and self.comparator(self.data[right], self.data[largest]):
            largest = right
        if largest != i:
            temp = self.data[i]
            self.data[i] = self.data[largest]
            self.data[largest] = temp
            self.max_heapify(largest)

    def build_max_heap(self):
        """
        Uses max_heapify in a bottom-up manner to convert an array into a max-heap.
        """
        self.heap_size = len(self.data)
        for i in range(self.heap_size / 2 - 1, -1, -1):
            self.max_heapify(i)

    def heapsort(self):
        """
        The heapsort algorithm works as follows: start by using build_max_heap to build a max-heap. Since the maximum
        element of the array is stored at the root, it can be put into its correct final position by exchanging it with
        the last element. If we now discard the last element from the heap, we can easily transform the elements in
        self.data[0:heap_size-1] into a max-heap simply by calling max_heapify on the root.
        """
        self.build_max_heap()
        for i in range(self.heap_size - 1, 0, -1):
            temp = self.data[0]
            self.data[0] = self.data[i]
            self.data[i] = temp
            self.heap_size -= 1
            self.max_heapify(0)

    def heap_maximum(self):
        """ Returns the root of the heap
        """
        return self.data[0]

    def heap_extract_max(self):
        """ Extracts the root node of the heap
        """
        if self.heap_size < 1:
            raise HeapError("heap underflow")
        max_value = self.data[0]
        self.data[0] = self.data[self.heap_size - 1]
        self.heap_size -= 1
        self.data = self.data[0:self.heap_size] # remove element from the array
        self.max_heapify(0)
        return max_value

    def heap_increase_key(self, i, key):
        """
        Updates the node at index i to its new value key. Because increasing the key may violate the max-heap property,
        traverses a path from this node to the root to find a proper place for the newly increased key
        """
        if self.is_heap_property_violation(key, self.data[i].key):
            raise HeapError("new key is smaller than current key")
        self.data[i].key = key
        while i > 0 and self.is_heap_property_violation(self.data[self.parent(i)].key, self.data[i].key):
            temp = self.data[i]
            self.data[i] = self.data[self.parent(i)]
            self.data[self.parent(i)] = temp
            i = self.parent(i)

    def is_heap_property_violation(self, node, child):
        """ Checks whether the sub-tree violates the max-heap property
        """
        return node != child and not self.comparator(node, child)

    def max_heap_insert(self, node):
        """
        Implements the insert operation by appending to the list a node of value negative infinity, and then
        calls heap_increase_key on this node to put it in its correct final position in the heap
        """
        key = node.key
        node.key = self.default_key
        self.heap_size += 1
        if self.heap_size > len(self.data):
            self.data.append(node)
        else:
            self.data[self.heap_size - 1] = node
        self.heap_increase_key(self.heap_size - 1, key)

    def parent(self, i):
        """ Returns the parent of heap element at index i """
        return (i - 1) / 2

    def left_child(self, i):
        """
        Returns the left child of the heap element at index i
        """
        return 2 * (i + 1) - 1

    def right_child(self, i):
        """
        Returns the right child of the heap element at index i
        """
        return 2 * (i + 1)

    def __str__(self):
        """
        Returns a string representation of a binary heap
        """
        s = ""
        if self.heap_size > 0:
            depth = 0
            max_depth = int(math.ceil(math.log(self.heap_size, 2)))
            while depth <= max_depth:
                for i in range(int(math.floor(2 ** (max_depth - depth - 1)))):
                    s += "\t"
                for i in range(2 ** depth - 1, 2 ** (depth + 1) - 1, 2):
                    if i < self.heap_size:
                        left = str(self.data[i])
                        s += left
                        for j in range(int(2 * math.floor(2 ** (max_depth - depth - 1)))):
                            s += "\t"
                        if i > 0 and i + 1 < self.heap_size:
                            right = str(self.data[i + 1])
                            s += right
                        for j in range(int(2 * math.floor(2 ** (max_depth - depth - 1)))):
                            s += "\t"
                s += "\n"
                depth += 1
        return s

class MinHeap(Heap):
    def __init__(self, data):
        super(MinHeap, self).__init__(data)
        self.comparator = lambda x, y: x < y
        self.default_key = float("inf")

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class HeapError(Error):
    """Exception raised for errors in the heap methods.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg

if __name__ == "__main__":
    import argparse
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Builds a binary heap')
    # add arguments
    parser.add_argument('values', metavar='N', type=int, nargs='+', help='a value for the heap')
    parser.add_argument('--min-heap', action='store_true', help='Builds a min-heap')
    parser.add_argument('--heapify', metavar='I', type=int, help='Calls max-heapify on the node')
    parser.add_argument('--sort', action='store_true', help='Sorts the values using heapsort')
    # parse arguments
    args = parser.parse_args()
    nodes = [Node(value, value) for value in args.values]
    h = MinHeap(nodes) if args.min_heap else Heap(nodes)
    if args.heapify:
        h.max_heapify(args.heapify)
    else:
        h.build_max_heap()
    if args.sort:
        h.heapsort()
        print h.data
    else:
        print h