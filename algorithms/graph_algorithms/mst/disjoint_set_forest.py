"""
disjoint_set_forest.py -- contains an implementation of a disjoint-set forest
"""

__author__ = 'Tom'

class DisjointSetForest:
    """ A data structure used to accumulate groups of nodes into sets using union-by-rank and path compression
    heuristics.
    """
    def __init__(self, nodes):
        """ Constructs a DisjointSetForest with a given list of nodes

        Attributes:

            nodes -- a list of nodes in the DisjointSetForest
        """
        self.nodes = nodes

    def make_set(self, x):
        """ Creates a new set whose only member is x.

        Attributes:

            x -- a node in the DisjointSetForest
        """
        x.parent = x
        x.rank = 0

    def union(self, x, y):
        """ Unites the sets that contain x and y into a new set that is the union of these two sets.

        Attributes:

            x -- a node in the DisjointSetForest
            y -- a different node in the DisjointSetForest
        """
        self.link(self.find_set(x), self.find_set(y))

    def link(self, x, y):
        """ Makes the node with greater height the parent of the node with lesser height. If the nodes have equal height
        the second becomes the parent and its rank gets incremented.

        Attributes:

            x -- a node in the DisjointSetForest
            y -- a different node in the DisjointSetForest
        """
        if x.rank > y.rank:
            y.parent = x
        else:
            x.parent = y
            if x.rank == y.rank:
                y.rank += 1

    def find_set(self, x):
        """ Returns a pointer to the representative of the set containing x.

        Attributes:

            x -- a node in the DisjointSetForest
        """
        if x != x.parent:
            x.parent = self.find_set(x.parent)
        return x.parent
