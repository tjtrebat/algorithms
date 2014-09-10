"""
Find the longest common subsequence of two sequences
"""

__author__ = 'Tom'

NORTHWEST, NORTH, WEST = 'NW', 'N', 'W'

class LCS:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.b = dict()

    def lcs_length(self):
        a = [0] * (len(self.y) + 1)
        for i in range(1, len(self.x) + 1):
            for j in range(1, len(self.y) + 1):
                if self.x[i - 1] == self.y[j - 1]:
                    c = a[j - 1] + 1
                    self.b[(i, j)] = NORTHWEST
                elif a[j] >= a[0]:
                    c = a[j]
                    self.b[(i, j)] = NORTH
                else:
                    c = a[0]
                    self.b[(i, j)] = WEST
                a[j - 1] = a[0]
                a[0] = c
            a[len(self.y)] = a[0]
            a[0] = 0

    def get_lcs(self, i, j):
        if not i or not j:
            return ""
        s = ""
        if self.b[(i, j)] == NORTHWEST:
            s += self.get_lcs(i - 1, j - 1)
            s += self.x[i - 1]
        elif self.b[(i, j)] == NORTH:
            s += self.get_lcs(i - 1, j)
        else:
            s += self.get_lcs(i, j - 1)
        return s

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Find the longest common subsequence of two sequences')
    parser.add_argument('sequence', metavar='X', help='A sequence')
    parser.add_argument('sequence1', metavar='Y', help='Another sequence')
    args = parser.parse_args()
    lcs = LCS(args.sequence, args.sequence1)
    lcs.lcs_length()
    print lcs.get_lcs(len(lcs.x), len(lcs.y))
