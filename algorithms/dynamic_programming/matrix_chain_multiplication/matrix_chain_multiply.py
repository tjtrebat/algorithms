"""
Find the optimal matrix-chain multiplication given a sequence of matrices.
"""

__author__ = 'Tom'

import os

class MatrixChainMultiply:
    def __init__(self, matrices=[]):
        self.matrices = matrices
        self.m, self.s = dict(), dict()

    def matrix_chain_order(self):
        for i in range(len(self.matrices)):
            self.m[(i, i)] = 0
        for l in range(2, len(self.matrices) + 1):
            for i in range(len(self.matrices) - l + 1):
                j = i + l - 1
                self.m[(i, j,)] = float("inf")
                for k in range(i, j):
                    q = self.m[(i, k)] + self.m[(k + 1, j)]
                    q += self.matrices[i].rows * self.matrices[k].cols * self.matrices[j].cols
                    if q < self.m[(i, j)]:
                        self.m[(i, j)] = q
                        self.s[(i, j)] = k

    def recursive_matrix_chain_order(self, i, j):
        if i == j:
            self.m[(i, j,)] = 0
        else:
            cost = float("inf")
            for k in range(i, j):
                cost = self.recursive_matrix_chain_order(i, k)
                cost += self.recursive_matrix_chain_order(k + 1, j)
                cost += self.matrices[i].rows * self.matrices[k].cols * self.matrices[j].cols
                if (i, j) not in self.m or cost < self.m[(i, j)]:
                    self.m[(i, j)] = cost
                    self.s[(i, j)] = k
        return self.m[(i, j)]

    def memoized_matrix_chain(self):
        for i in range(len(self.matrices)):
            for j in range(i, len(self.matrices)):
                self.m[(i, j)] = float("inf")
        return self.lookup_chain(0, len(self.matrices) - 1)

    def lookup_chain(self, i, j):
        if self.m[(i, j)] < float("inf"):
            return self.m[i, j]
        if i == j:
            self.m[(i, j)] = 0
        else:
            for k in range(i, j):
                q = self.lookup_chain(i, k) + self.lookup_chain(k + 1, j)
                q += self.matrices[i].rows * self.matrices[k].cols * self.matrices[j].cols
                if q < self.m[(i, j)]:
                    self.m[(i, j)] = q
        return self.m[(i, j)]

    def print_optimal_parens(self, i, j):
        if i == j:
            return str(self.matrices[i])
        s = "("
        s += self.print_optimal_parens(i, self.s[i, j])
        s += self.print_optimal_parens(self.s[i, j] + 1, j)
        s += ")"
        return s

    def get_product(self, i, j):
        if i == j:
            return self.matrices[i]
        return self.get_product(i, self.s[i, j]) * self.get_product(self.s[i, j] + 1, j)

class Matrix:
    def __init__(self, rows, cols, data={}, label=None):
        self.rows = rows
        self.cols = cols
        self.label = label
        self.data = data

    @classmethod
    def read_matrix(cls, lines, label=None):
        if isinstance(lines, file):
            lines = lines.read()
        lines = lines.strip().split("\n")
        data = {}
        rows, cols = 0, 0
        for line in lines:
            if line.strip():
                cols = 0
                for num in line.split():
                    try:
                        data[(rows, cols)] = float(num)
                        cols += 1
                    except ValueError:
                        pass
                rows += 1
        return Matrix(rows, cols, data=data, label=label)

    def write_matrix(self, outfile=None):
        lines = ""
        for i in range(self.rows):
            for j in range(self.cols):
                lines += str(self.data[(i, j)]) + "\t"
            lines += "\n"
        if outfile is not None:
            if not isinstance(outfile, file):
                outfile = file(outfile, 'w')
            outfile.write(lines)
        return lines

    def __mul__(self, other):
        if self.cols != other.rows:
            raise MatrixError("Incompatible dimensions")
        c = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                c.data[(i, j)] = 0
                for k in range(self.cols):
                    c.data[(i, j)] += self.data[(i, k)] * other.data[(k, j)]
        return c

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.label)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MatrixError(Error):
    """Exception raised for errors in the heap methods.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Find the optimal parenthesization of a matrix-chain multiplication')
    parser.add_argument('infiles', metavar='F', type=argparse.FileType('r'), nargs='+', help='A list of files')
    parser.add_argument('--product', action='store_true', help='multiply the matrices (default: find optimal parens.)')
    args = parser.parse_args()
    lbl = 65
    mcm = MatrixChainMultiply()
    for infile in args.infiles:
        m = Matrix.read_matrix(infile, label=chr(lbl))
        mcm.matrices.append(m)
        lbl += 1
    mcm.matrix_chain_order()
    if args.product:
        product = mcm.get_product(0, len(mcm.matrices) - 1)
        print product.write_matrix()
    else:
        print mcm.print_optimal_parens(0, len(mcm.matrices) - 1)
