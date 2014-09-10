"""
mst_canvas.py -- Draw the minimum-spanning-tree of randomly-chosen points on a plane.
"""

__author__ = 'Tom'

import math
import random
from Tkinter import *
import prim, kruskal

class MstCanvas:
    """
    A class used to calculate and draw the edges forming a minimum-spanning-tree amongst nodes in an xy plane.
    """
    def __init__(self, root):
        """ Constructs a new MstCanvas object

        Attributes:

            root -- a Tk object
            nodes -- a list of Nodes
            edges -- a list of Edges
        """
        self.root = root
        self.setup()

    def setup(self):
        """ Configures the Tk and Canvas objects """
        self.root.title("MST")
        self.root.resizable(0, 0)
        self.canvas = Canvas(self.root, width=500, height=500)
        self.canvas.pack(fill='both', expand='yes')
        self.canvas.configure(bg="white")

    def kruskal(self, nodes):
        """
        Draws the edges using Kruskal's algorithm
        """
        k = kruskal.Kruskal(nodes, self.get_edges(nodes))
        self.draw_lines(k.mst())

    def prim(self, nodes):
        """
        Draws the edges using Prim's algorithm
        """
        p = prim.Prim(nodes, self.get_edges(nodes))
        p.mst(0)
        self.draw_lines(p.get_mst_edges())

    def draw_lines(self, mst):
        """ Draws lines onto a Canvas given a list of edges whose node values are coordinates on the xy plane
        """
        for line in mst:
            self.canvas.create_line(line[0].value, line[1].value)

    def get_edges(self, nodes):
        edges = dict()
        for node in nodes:
            for other_node in nodes:
                if node != other_node:
                    edges[(node, other_node)] = math.hypot(
                        node.value[0] - other_node.value[0],
                        node.value[1] - other_node.value[1])
        return edges

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Draws the minimum-spanning-tree of randomly-chosen points on a plane')
    # add arguments
    parser.add_argument('--points', metavar='P', type=int, default=1500, help='the number of points')
    parser.add_argument('--prim', action='store_true', help='use Prim\'s algorithm instead')
    # parse arguments
    args = parser.parse_args()
    # use a Graph create the Edges from a list of Nodes
    g = Graph()
    # Draw the minimum-spanning-tree on a Tk Canvas with the appropriate algorithm
    root = Tk()
    gui = MstCanvas(root)
    nodes = [] # a list of Nodes
    if args.prim: # use prim's algorithm
        # add to nodes a Node with random point value
        for i in range(args.points):
            nodes.append(prim.Node((random.randint(0, 500), random.randint(0, 500),)))
        for node in nodes:
            for other_node in nodes:
                if node != other_node:
                    node.adjacent_nodes.append(other_node)
        gui.prim(nodes)
    else: # default to using kruskal
        # add to nodes a Node with random point value
        for i in range(args.points):
            nodes.append(kruskal.Node((random.randint(0, 500), random.randint(0, 500),)))
        gui.kruskal(nodes)
    root.mainloop()