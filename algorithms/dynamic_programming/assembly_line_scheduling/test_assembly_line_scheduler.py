from unittest import TestCase
from algorithms.dynamic_programming.assembly_line_scheduling.assembly_line_scheduling import *

__author__ = 'Tom'

class TestAssemblyLineScheduler(TestCase):
    def setUp(self):
        assembly_lines = read_assembly_lines_from_file(file('./data/assembly-lines'))
        if assembly_lines is not None:
            self.als = AssemblyLineScheduler(*assembly_lines)
        self.f_star = 38
        self.l_star = 0

    def test_fastest_way(self):
        self.als.fastest_way()
        self.assertEquals(self.als.fastest_time, self.f_star)
        self.assertEquals(self.als.fastest_line, self.l_star)

    def test_fastest_way_recursive(self):
        self.als.fastest_way_recursive()
        self.assertEquals(self.als.fastest_time, self.f_star)
        self.assertEquals(self.als.fastest_line, self.l_star)
