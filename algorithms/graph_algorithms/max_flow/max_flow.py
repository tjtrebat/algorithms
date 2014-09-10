"""
Finds a maximum flow of a flow network.
"""

__author__ = 'Tom'

from algorithms.graph_algorithms.bfs import bfs

class MaxFlow:
    def __init__(self, nodes, capacities):
        self.nodes = nodes
        self.capacities = capacities
        self.flows = dict()
        self.residual = dict()
        for key, value in self.capacities.iteritems():
            self.flows[key] = 0
            self.residual[key] = value

    def max_flow(self):
        path = self.get_augmenting_path()
        while path is not None:
            min_edge = min([self.residual[edge] for edge in path])
            for u, v in path:
                self.flows[(u, v)] += min_edge
                self.residual[(u, v)] -= min_edge
                if not self.residual[(u, v)]: # remove a residual edge
                    self.residual.pop((u, v))
                    u.adjacent_nodes.remove(v)
                if (v, u) not in self.residual: # adds a residual edge
                    self.residual[(v, u)] = 0
                    v.adjacent_nodes.append(u)
                self.residual[(v, u)] += min_edge
            path = self.get_augmenting_path()

    def get_augmenting_path(self):
        searcher = bfs.BFS(self.nodes)
        s, t = self.nodes[0], self.nodes[len(self.nodes) - 1]
        searcher.search(s)
        path = list()
        while t.parent is not None:
            path.append((t.parent, t,))
            t = t.parent
        if t == s:
            return path

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Finds the maximum flow of a graph')
    # add arguments
    parser.add_argument('infile', type=argparse.FileType('r'))
    # parse arguments
    args = parser.parse_args()
    # read in edge weights from file
    g = Graph()
    g.read_graph(args.infile)
    nodes = [bfs.Node(chr(i)) for i in range(ord('r'), ord('r') + g.num_nodes)]
    for i, j in g.edge_weights.keys():
        nodes[i].adjacent_nodes.append(nodes[j])
    capacities = dict()
    for key, value in g.edge_weights.iteritems():
        capacities[(nodes[key[0]], nodes[key[1]])] = value
    mf = MaxFlow(nodes, capacities)
    mf.max_flow()
    for key, value in mf.flows.iteritems():
        print key, "%d/%d" % (value, mf.capacities[key],)