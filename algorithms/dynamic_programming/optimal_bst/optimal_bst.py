"""
Find the optimal binary search tree based on probabilities of keys.
"""

__author__ = 'Tom'

class OptimalBST:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.root = dict()

    def optimal_bst(self, n):
        e = dict()
        w = dict()
        for i in range(1, n + 2):
            e[(i, i - 1)] = self.q[i - 1]
            w[(i, i - 1)] = self.q[i - 1]
        for l in range(1, n + 1):
            for i in range(1, n - l + 2):
                j = i + l - 1
                e[(i, j)] = float("inf")
                w[(i, j)] = w[(i, j - 1)] + self.p[j - 1] + self.q[j]
                for r in range(i, j + 1):
                    t = round(e[(i, r - 1)] + e[(r + 1, j)] + w[(i, j)], 2)
                    if t < e[(i, j)]:
                        e[(i, j)] = t
                        self.root[(i, j)] = r
        return e

    def construct_optimal_bst(self, i, j):
        k = self.root[(i, j)]
        if len(self.p) == j - i + 1:
            print "k[%d] is the root" % k
        if i <= k - 1:
            print "k[%d] is the left child of k[%d]" % (self.root[(i, k - 1)], k)
            self.construct_optimal_bst(i, k - 1)
        else:
            print "d[%d] is the left child of k[%d]" % (i - 1, k)
        if k + 1 <= j:
            print "k[%d] is the right child of k[%d]" % (self.root[(k + 1, j)], k)
            self.construct_optimal_bst(k + 1, j)
        else:
            print "d[%d] is the right child of k[%d]" % (j, k)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Find the optimal binary search tree based on probabilities of keys')
    parser.add_argument('--p', metavar='P', type=float, nargs='+',
        help='A list of probabilities of each key', required=True)
    parser.add_argument('--q', metavar='Q', type=float, nargs='+',
        help='A list of probabilities of each dummy key', required=True)
    args = parser.parse_args()
    bst = OptimalBST(args.p, args.q)
    bst.optimal_bst(len(args.p))
    bst.construct_optimal_bst(1, len(bst.p))


