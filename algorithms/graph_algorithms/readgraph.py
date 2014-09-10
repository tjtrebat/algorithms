"""
read_graph.py -- Used for reading graph node and edge information from an adjacency matrix contained within a file.
"""

__author__ = 'Tom'

class Graph:
    def __init__(self):
        self.num_nodes = 0
        self.edge_weights = dict()

    def read_graph(self, infile):
        """
        Reads a file to populate the nodes and edges in a Graph.

        Attributes:

            filename -- a file containing edge weights
        """
        if isinstance(infile, str):
            infile = open(infile, 'r')
        text_unicode = unicode(infile.read(), "utf-8").strip() # reads in unicode text
        # Split the text on the newline character.
        lines = text_unicode.split("\n")
        self.num_nodes = len(lines)
        self.edge_weights = dict()
        for i, line in enumerate(lines):
            for j, edge_weight in enumerate(line.split("\t")):
                if j < self.num_nodes:
                    if Graph.is_float(edge_weight): # an edge exists between the two nodes
                        self.edge_weights[(i, j)] = float(edge_weight)

    def compute_transpose(self):
        t = dict()
        for i, j in self.edge_weights.keys():
            t[(j, i)] = self.edge_weights[(i, j)]
        return t

    @staticmethod
    def is_float(weight):
        """ Returns True if weight is a valid floating-point number

        Attributes:

            weight -- an edge weight
        """
        try:
            float(weight)
            return True
        except ValueError:
            pass
        return False

    def has_edge(self, u, v):
        try:
            edge = self.edge_weights[(u, v)]
        except KeyError:
            return False
        return True

    def __unicode__(self):
        """
        Prints the graph with a non-ascii character for positive infinity
        """
        s = ""
        for i in self.num_nodes:
            for j in self.num_nodes:
                if self.has_edge(i, j):
                    s += "%04.1f" % self.edge_weights[(i, j)]
                else:
                    s += "%*s%s%*s" % (1, " ", u"\u221E", 3, " ",)
                s += "\t"
            s += "\n"
        return s