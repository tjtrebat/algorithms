"""
 prim.py -- Implements Prims's algorithm for finding a minimum-spanning-tree
 """

__author__ = 'Tom'

from algorithms.sorting.heapsort import heapsort

class Node(heapsort.Node):
    """ Represents a node in a graph
    """
    def __init__(self, value):
        """ Constructs a Node with a given value

        Attributes:

            value -- a value for the node
        """
        super(Node, self).__init__(value)
        self.adjacent_nodes = []

    def __repr__(self):
        """ A representation of a Node
        """
        return repr(self.value)

class Prim:
    """ Prim computes a minimum-spanning-tree of a weighted, undirected graph by adding a light edge to the tree that
    connects an isolated vertex.
    """
    def __init__(self, nodes, edges):
        """ Contructs a new Prim object.

        Attributes:
            nodes -- a list of Nodes
        """
        self.nodes = nodes
        self.edges = edges

    def mst(self, r):
        """ Calculates the minimum-spanning-tree
        """
        # make each node's key positive infinity and sets the parent to None
        for node in self.nodes:
            node.key = float("inf")
            node.parent = None
        # allocates a binary min-heap for the nodes based on its key
        q = heapsort.MinHeap([node for node in self.nodes])
        # decrease the key of the root node
        q.heap_increase_key(r, 0)
        # Extract nodes from q. For each adjacent node, check whether the weight of the edge
        # connecting the nodes is less than the node's key. If so, update the node's key to reflect
        # the new edge crossing the cut having less edge weight.
        while len(q.data) > 0:
            u = q.heap_extract_max() # extracts the node with the smallest key
            # go through each adjacent node not in the tree and update its
            # key and parent if a light edge exists between the two nodes
            for v in u.adjacent_nodes:
                edge_weight = self.edges[(u, v)]
                if v in q.data and edge_weight < v.key:
                    v.parent = u
                    q.heap_increase_key(q.data.index(v), edge_weight)

    def get_mst_edges(self):
        """ Returns a list of edges that compose the minimum-spanning-tree
        """
        mst = []
        for node in self.nodes:
            if node.parent is not None:
                mst.append((node.parent, node,))
        return mst

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Computes the minimum-spanning-tree of a connected, ' \
                                                 'undirected graph using Prim\'s algorithm')
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
        nodes[i].adjacent_nodes.append(nodes[j])
    # use Prim's algorithm to compute mst a minimum-spanning-tree
    p = Prim(nodes, edges)
    p.mst(0)
    print p.get_mst_edges()