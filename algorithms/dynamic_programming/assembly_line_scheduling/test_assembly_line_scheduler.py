from unittest import TestCase
from algorithms.dynamic_programming.assembly_line_scheduling.assembly_line_scheduling import *

__author__ = 'Tom'

class TestAssemblyLineScheduler(TestCase):
    def setUp(self):
        infiles = [file('./data/assembly-lines'), file('./data/assembly-lines-1'),]
        self.assembly_line_schedulers = []
        for infile in infiles:
            assembly_lines = read_assembly_lines_from_file(infile)
            if assembly_lines is not None:
                self.assembly_line_schedulers.append(AssemblyLineScheduler(*assembly_lines))
        self.f_star = [38, 35,]
        self.l_star = [0, 0,]

    def test_fastest_way(self):
        for i, als in enumerate(self.assembly_line_schedulers):
            als.fastest_way()
            self.assertEquals(als.fastest_time, self.f_star[i])
            self.assertEquals(als.fastest_line, self.l_star[i])

    def test_fastest_way_recursive(self):
        for i, als in enumerate(self.assembly_line_schedulers):
            als.fastest_way_recursive()
            self.assertEquals(als.fastest_time, self.f_star[i])
            self.assertEquals(als.fastest_line, self.l_star[i])




