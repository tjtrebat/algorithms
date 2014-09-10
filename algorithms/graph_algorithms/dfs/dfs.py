"""
Performs depth-first search on the graph specified by infile and outputs the biconnected and strongly-connected
components.
"""

__author__ = 'Tom'

TREE, FORWARD, BACK, CROSS = 0, 1, 2, 3

class Node:
    def __init__(self, value):
        self.value = value
        self.d = None
        self.f = None
        self.parent = None
        self.adjacent_nodes = list()
        self.visited = False
        self.low = None
        self.articulation = False
        self.separators = 0
        self.descendants = 0

    def __repr__(self):
        return repr(self.value)

class DFS:
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = dict()

    def search(self):
        for u in self.nodes:
            u.visited = False
            u.parent = None
        self.time = 0
        self.scc = dict()
        self.num_components = 0
        self.bcc_edges = list()
        self.bccs = dict()
        self.num_bcc = 0
        for u in sorted(self.nodes, key=lambda x: x.f, reverse=True):
            if not u.visited:
                self.scc[self.num_components] = list((u,))
                self.visit(u)
                self.num_components += 1
                if u.separators < 2:
                    u.articulation = False

    def visit(self, u):
        u.visited = True
        self.time += 1
        u.d = self.time
        u.low = u.d
        for v in u.adjacent_nodes:
            if not v.visited:
                self.edges[(u, v)] = TREE
                self.scc[self.num_components].append(v)
                self.bcc_edges.append((u, v,))
                v.parent = u
                self.visit(v)
                u.descendants += 1 + v.descendants
                if v.low >= u.d:
                    self.bccs[self.num_bcc] = list()
                    done = False
                    while not done:
                        e = self.bcc_edges.pop()
                        self.bccs[self.num_bcc].append(e)
                        if e == (u, v,):
                            done = True
                    self.num_bcc += 1
                    u.articulation = True
                    u.separators += 1
                u.low = min(u.low, v.low)
            elif u.parent != v and v.d < u.d:
                # (u, v) is a back edge from u to its ancestor v
                self.bcc_edges.append((u, v,))
                u.low = min(u.low, v.d)
        self.time += 1
        u.f = self.time

if __name__ == "__main__":
    import argparse
    from algorithms.graph_algorithms.readgraph import Graph
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Performs depth-first search amongst nodes in a graph.')
    # add arguments
    parser.add_argument('infile', type=argparse.FileType())
    # parse arguments
    args = parser.parse_args()
    # read in edge weights from file
    g = Graph()
    g.read_graph(args.infile)
    nodes = [Node(chr(i)) for i in range(ord('a'), ord('a') + g.num_nodes)]
    for i, j in g.edge_weights.keys():
        nodes[i].adjacent_nodes.append(nodes[j])
    dfs = DFS(nodes)
    dfs.search()
    # output node discovery and finish times
    d, f = "", ""
    for node in nodes:
        d += str(node.d).ljust(10)
        f += str(node.f).ljust(10)
    print "V".ljust(10) + "".join(map(lambda x: x.value.ljust(10), nodes))
    print "d[V]".ljust(10) + d
    print "f[V]".ljust(10) + f
    # output articulation pts.
    print "\nArticulation Pts.: %s" % ", ".join(map(lambda u: u.value, filter(lambda u: u.articulation, nodes)))
    # output biconnected components
    print "\nNo. of biconnected components: %d" % dfs.num_bcc
    for i, edges in dfs.bccs.iteritems():
        vertices = list()
        for u, v in edges:
            if u.value not in vertices:
                vertices.append(u.value)
            if v.value not in vertices:
                vertices.append(v.value)
        print "%d: %s" % (i + 1, ", ".join(vertices),)
    # output classification of edges
    print "\nClassification of edges:"
    for u in nodes:
        for v in u.adjacent_nodes:
            if (u, v,) not in dfs.edges or dfs.edges[(u, v)] != TREE:
                if u.d < v.d <= u.d + u.descendants:
                    dfs.edges[(u, v)] = FORWARD
                elif v.d < u.d <= v.d + v.descendants:
                    dfs.edges[(u, v)] = BACK
                else:
                    dfs.edges[(u, v)] = CROSS
    for edge, classification in dfs.edges.iteritems():
        if not classification:
            classification = "Tree"
        elif classification < 2:
            classification = "Forward"
        elif classification < 3:
            classification = "Back"
        else:
            classification = "Cross"
        print "%s is a %s edge." % (edge, classification,)
    # output strongly-connected components
    for node in nodes:
        node.adjacent_nodes = list()
    for i, j in g.edge_weights.keys():
        nodes[j].adjacent_nodes.append(nodes[i])
    dfs.search()
    print "\nNo. of strongly-connected components: %d" % dfs.num_components
    for i, vertices in dfs.scc.iteritems():
        print "%d: %s" % (i + 1, ", ".join(map(lambda x: x.value, vertices)),)


