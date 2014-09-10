from unittest import TestCase
from algorithms.sorting.heapsort.heapsort import *

__author__ = 'Tom'

class TestHeap(TestCase):
    def setUp(self):
        self.h = Heap([Node(value, value) for value in [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]])

    def test_max_heapify(self):
        self.h.max_heapify(1)
        self.is_max_heap()

    def test_build_max_heap(self):
        self.h.build_max_heap()
        self.is_max_heap()

    def test_heapsort(self):
        self.h.heapsort()
        max_value = float("-inf")
        for node in self.h.data:
            self.assertGreaterEqual(node.key, max_value)
            max_value = node.key

    def test_heap_maximum(self):
        self.h.build_max_heap()
        max_value = self.h.heap_maximum()
        for node in self.h.data: # check if max_value greater than all the other elements in the array
            self.assertGreaterEqual(max_value, node)

    def test_heap_extract_max(self):
        self.h.build_max_heap()
        max_value = float("inf")
        while self.h.heap_size > 0:
            extracted = self.h.heap_extract_max()
            self.assertLessEqual(extracted.key, max_value)
            max_value = extracted.key

    def test_heap_increase_key(self):
        self.h.build_max_heap()
        self.h.heap_increase_key(self.h.heap_size - 1, 17)
        self.is_max_heap()

    def test_max_heap_insert(self):
        self.h.build_max_heap()
        self.h.max_heap_insert(Node(12, key=12))
        self.is_max_heap()

    def is_max_heap(self):
        for i, node in enumerate(self.h.data):
            left = self.h.left_child(i)
            if left < self.h.heap_size:
                self.assertGreaterEqual(node, self.h.data[left])
            right = self.h.right_child(i)
            if right < self.h.heap_size:
                self.assertGreaterEqual(node, self.h.data[right])

    def test_left_child(self):
        for i in range(len(self.h.data)):
            try:
                self.assertEqual(self.h.data[2 * (i + 1) - 1], self.h.data[self.h.left_child(i)])
            except IndexError:
                pass

    def test_right_child(self):
        for i in range(len(self.h.data)):
            try:
                self.assertEqual(self.h.data[2 * (i + 1)], self.h.data[self.h.right_child(i)])
            except IndexError:
                pass