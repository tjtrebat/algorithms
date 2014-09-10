"""
 kruskal.py -- Implements Kruskal's algorithm for finding a minimum-spanning-tree
"""

__author__ = 'Tom'

from disjoint_set_forest import DisjointSetForest

class Node:
    """ Represents a node in a disjoint-set forest
    """
    def __init__(self, value):
        """ Constructs a Node with a given value

        Attributes:

            value -- a value for the node
        """
        self.value = value
        self.rank = -1
        self.parent = None

    def __repr__(self):
        """ A representation of a Node
        """
        return repr(self.value)

class Kruskal:
    """ Kruskal computes a minimum-spanning-tree of a weighted, undirected graph by adding a safe edge of least weight.
    """
    def __init__(self, nodes, edges):
        """ Contructs a new Kruskal object.

        Attributes:
            nodes -- a list of Nodes
            edges -- a dict of edge weights
        """
        self.dsf = DisjointSetForest(nodes)
        self.edges = edges

    def mst(self):
        """ Returns the minimum-spanning-tree mst of the edges
        """
        # sets each node's parent to itself and the rank 0
        for node in self.dsf.nodes:
            self.dsf.make_set(node)
        # Go through each of the edges in non-decreasing order by weight.
        # If the nodes that make up the edge are not in the same set, perform a
        # union operation amongst the two nodes and add the edge to mst.
        mst = []
        for u, v in sorted(self.edges.keys(), key=lambda x: self.edges[x]):
            if self.dsf.find_set(u) != self.dsf.find_set(v):
                mst.append((u, v,))
                self.dsf.union(u, v)
        return mst

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Computes the minimum-spanning-tree of a connected, '\
                                                 'undirected graph using Kruskal\'s algorithm')
    # add arguments
    parser.add_argument('infile', type=argparse.FileType('r'))
    # parse arguments
    args = parser.parse_args()
    # read in edge weights from file
    g = Graph()
    g.read_graph(args.infile)
    nodes = [Node(chr(i)) for i in range(ord('a'), ord('a') + g.num_nodes)]
    edges = dict()
    for i, j in g.edge_weights.keys():
        edges[(nodes[i], nodes[j])] = g.edge_weights[(i, j)]
    # use Kruskal's algorithm to compute a minimum-spanning-tree
    k = Kruskal(nodes, edges)
    print k.mst() # prints the tree