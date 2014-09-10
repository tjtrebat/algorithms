"""
test_mst.py -- tests the kruskal and prim modules
"""

from unittest import TestCase
from algorithms.graph_algorithms.readgraph import Graph
from algorithms.graph_algorithms.mst import kruskal
from algorithms.graph_algorithms.mst import prim

__author__ = 'Tom'

class TestMst(TestCase):
    """ Test the minimum-spanning-tree functions """
    def setUp(self):
        self.g = Graph() # a graph object for reading graph nodes and edges
        # create a dict of graph files to minimum-spanning-tree total weight
        self.graphname_weights = {'./graph': 37, './graph1': 14}

    def test_kruskal(self):
        """ Tests if kruskal produces a minimum-spanning-tree by summing up all the edge weights. """
        # For each graph, see if the total edge weight of the mst is at a minimal.
        for fname, weight in self.graphname_weights.iteritems():
            self.g.read_graph(fname) # read the graph
            nodes = [kruskal.Node(chr(i)) for i in range(ord('a'), ord('a') + self.g.num_nodes)]
            edges = dict()
            for i, j in self.g.edge_weights.keys():
                edges[(nodes[i], nodes[j])] = self.g.edge_weights[(i, j)]
            k = kruskal.Kruskal(nodes, edges) # create a Kruskal object
            total_weight = sum(map(lambda edge: k.edges[edge], k.mst())) # get total edge weights in mst
            self.assertEqual(total_weight, weight) # check if the total is minimized

    def test_prim(self):
        """ Tests if prim produces a minimum-spanning-tree by summing up all the edge weights. """
        for fname, weight in self.graphname_weights.iteritems():
            self.g.read_graph(fname) # read the graph
            nodes = [prim.Node(chr(i)) for i in range(ord('a'), ord('a') + self.g.num_nodes)]
            edges = dict()
            for i, j in self.g.edge_weights.keys():
                edges[(nodes[i], nodes[j])] = self.g.edge_weights[(i, j)]
                nodes[i].adjacent_nodes.append(nodes[j])
            p = prim.Prim(nodes, edges) # create a Kruskal object
            p.mst(0)
            total_weight = sum(map(lambda edge: p.edges[edge], p.get_mst_edges())) # get total edge weights in mst
            self.assertEqual(total_weight, weight) # check if the total is minimized