"""
A breadth-first searcher.
"""

__author__ = 'Tom'

class Node:
    def __init__(self, value):
        self.value = value
        self.d = None
        self.parent = None
        self.adjacent_nodes = list()

    def __repr__(self):
        return repr(self.value)

class BFS:
    def __init__(self, nodes):
        self.nodes = nodes

    def search(self, s):
        # initialize each node
        for node in self.nodes:
            node.d = float("inf")
            node.parent = None
        # discover the source node
        s.d = 0
        s.parent = None
        q = list()
        # append source node to list so we can discover its adjacent nodes
        q.append(s)
        while q:
            u = q.pop(0) # pop the first element
            # discover each adjacent node and append to q
            for v in u.adjacent_nodes:
                if v.d == float("inf"): # marks node as discovered
                    v.d = u.d + 1 # increments distance of v to source
                    v.parent = u # sets v's predecessor to u
                    q.append(v)

    def print_path(self, s, v):
        if v == s:
            print s
        elif v.parent is None:
            print "no path from %s to %s exists" % (s, v,)
        else:
            self.print_path(s, v.parent)
            print v

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Performs breadth-first search on a graph.')
    # add arguments
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--source', type=int, default=1, help='A source vertex')
    parser.add_argument('--dest', type=int, help='A destination vertex')
    # parse arguments
    args = parser.parse_args()
    # read in edge weights from file
    g = Graph()
    g.read_graph(args.infile)
    nodes = [Node(chr(i)) for i in range(ord('r'), ord('r') + g.num_nodes)]
    for i, j in g.edge_weights.keys():
        nodes[i].adjacent_nodes.append(nodes[j])
    bfs = BFS(nodes)
    s = nodes[args.source]
    bfs.search(s)
    if args.dest:
        d = nodes[args.dest]
        print "shortest-path from %s to %s" % (s, d)
        bfs.print_path(s, d)
    else:
        # print shortest-paths from source to every other vertex in the graph
        for node in nodes:
            if node != s:
                print "shortest-path from %s to %s" % (s, node)
                bfs.print_path(s, node)