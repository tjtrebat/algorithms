"""
Find the fastest way through a factory using recursive and dynamic programming techniques.
"""

__author__ = 'Tom'

class AssemblyLineScheduler:
    def __init__(self, line1, line2, num_stations):
        """ Constructs an AssemblyLineScheduler.

        Attributes:
            line1 -- the first line
            line2 -- the second line
            num_stations -- the number of stations per line
        """
        self.num_stations = num_stations
        self.assembly_lines = (line1, line2,)

    def fastest_way(self):
        """ Find the fastest way through a factory using dynamic programming.
        """
        # For each line, calculate the fastest time to the first station by
        # summing the line's entry time with the assembly time.
        for line in self.assembly_lines:
            line.fastest_times[0] = line.entry_time + line.stations[0].assembly_time
        # Determine the fastest time to the remaining stations in the factory. For each station, use the fastest time
        # from the previous station on the same line, or use the fastest time from the previous station on the other
        # line plus the transfer time, to calculate the fastest time.
        for j in range(1, self.num_stations):
            for i, line in enumerate(self.assembly_lines):
                other_line = self.assembly_lines[(i + 1) % 2] # variable for the other assembly line
                station, other_station = line.stations[j], other_line.stations[j - 1] # variables for previous stations
                # fastest time to the previous station on the same line
                line_time = line.fastest_times[j - 1]
                # fastest time to the previous station on the other line plus the transfer time
                other_line_time = other_line.fastest_times[j - 1] + other_station.transfer_time
                if line_time <= other_line_time:
                    line.fastest_times[j] = line_time + station.assembly_time
                    line.fastest_lines[j - 1] = i + 1
                else:
                    line.fastest_times[j] = other_line_time + station.assembly_time
                    line.fastest_lines[j - 1] = ((i + 1) % 2) + 1
        # Calculate the fastest time and line after exiting.
        self.fastest_time = float("inf")
        for i, line in enumerate(self.assembly_lines):
            finishing_time = line.fastest_times[self.num_stations - 1] + line.exit_time
            if finishing_time < self.fastest_time:
                self.fastest_time = finishing_time
                self.fastest_line = i + 1

    def recursive_fastest_way(self, n, line):
        """ A recursive solution to fastest_way.
        """
        if n == self.num_stations:
            t_line1 = self.recursive_fastest_way(n - 1, 0) + self.assembly_lines[0].exit_time
            t_line2 = self.recursive_fastest_way(n - 1, 1) + self.assembly_lines[1].exit_time
            if t_line1 <= t_line2:
                self.fastest_time = t_line1
                self.fastest_line = 1
            else:
                self.fastest_time = t_line2
                self.fastest_line = 2
            return self.fastest_time
        else:
            if not n:
                fastest_time = (self.assembly_lines[line].stations[n].assembly_time
                                + self.assembly_lines[line].entry_time)
            else:
                other_line = (line + 1) % len(self.assembly_lines)
                assembly_time = self.assembly_lines[line].stations[n].assembly_time
                t_same_line = self.recursive_fastest_way(n - 1, line) + assembly_time
                t_diff_line = (self.recursive_fastest_way(n - 1, other_line)
                               + self.assembly_lines[other_line].stations[n - 1].transfer_time + assembly_time)
                if t_same_line <= t_diff_line:
                    if n:
                        self.assembly_lines[line].fastest_lines[n - 1] = line + 1
                    fastest_time = t_same_line
                else:
                    if n:
                        self.assembly_lines[line].fastest_lines[n - 1] = other_line + 1
                    fastest_time = t_diff_line
            self.assembly_lines[line].fastest_times[n] = fastest_time
        return self.assembly_lines[line].fastest_times[n]

    def print_stations(self):
        """ Prints the fastest way through the factory.
        """
        i = self.fastest_line
        print "line %d, station %d" % (i, self.num_stations,)
        for j in range(self.num_stations - 2, -1, -1):
            i = self.assembly_lines[i - 1].fastest_lines[j]
            print "line %d, station %d" % (i, j + 1,)

    def print_stations_in_order(self, j):
        """ Prints the fastest way through the station in order.
        """
        if j == self.num_stations - 1:
            line = self.fastest_line
        else:
            line = self.assembly_lines[self.print_stations_in_order(j + 1) - 1].fastest_lines[j]
        return line

    @classmethod
    def read_assembly_lines(cls, infile):
        """ Reads in AssemblyLines from a file and returns an AssemblyLineScheduler.
        """
        lines = infile.read().split("\n")
        a1 = AssemblyLine.read_assembly_line(lines[:3])
        a2 = AssemblyLine.read_assembly_line(lines[3:])
        return AssemblyLineScheduler(a1, a2, len(a1.stations))

    def __str__(self):
        """ A string representation of a factory showing assembly and transfer times of the stations.
        """
        s = ""
        s += "\t%s\n" % str(self.assembly_lines[0])
        s += "%s%s%s\n" % (str(self.assembly_lines[0].entry_time),
                               "\t" * (len(self.assembly_lines[0].stations) + 1),
                                self.assembly_lines[0].exit_time,)
        for station in self.assembly_lines[0].stations:
            if station.transfer_time is not None:
                s += "\t  " + str(station.transfer_time)
        s += "\n"
        for station in self.assembly_lines[1].stations:
            if station.transfer_time is not None:
                s += "\t  " + str(station.transfer_time)
        s += "\n"
        s += "%s%s%s\n" % (str(self.assembly_lines[1].entry_time),
                               "\t" * (len(self.assembly_lines[1].stations) + 1),
                               self.assembly_lines[1].exit_time,)
        s += "\t%s\n" % str(self.assembly_lines[1])
        return s

class AssemblyLine:
    """ Represents an assembly line in a factory with associated entry and exit times, as well as arrays for holding
    the fastest times to each of, and the lines used to arrive at, the stations.
    """
    def __init__(self, entry_time, exit_time, stations):
        """Contructs an AssemblyLine with given entry, exit and assembly times at each station.

        Attributes:

            entry_time -- an entry time
            exit_time -- an exit time
            stations -- a list of Stations
        """
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.stations = stations
        self.fastest_times = [0] * len(stations)
        self.fastest_lines = [-1] * (len(stations) - 1)

    @classmethod
    def read_assembly_line(cls, txt):
        """ Reads a line of text and returns an AssemblyLine with an entry and exit time and a list of Station objects
        that represent an individual station on the assembly line.
        """
        # get the entry, exit times from the first line of text
        entry_time, exit_time = map(int, txt[0].split(" "))
        # get the transfer times between stations on separate lines
        transfers = map(int, txt[2].split(" "))
        # initialize an array of Station objects by reading in the second line of values denoting assembly time at each
        # of the stations.
        stations = []
        for i, at in enumerate(map(int, txt[1].split(" "))):
            if i < len(transfers):
                stations.append(Station(at, transfers[i]))
            else:
                stations.append(Station(at))
        return AssemblyLine(entry_time, exit_time, stations)

    def __str__(self):
        """ A string representation of the AssemblyLine showing stations belonging to it separated by a whitespace
        character.
        """
        s = ""
        for station in self.stations:
            s += "%s\t" % station
        return s

class Station:
    """ An object used to denote a station on an AssemblyLine. Contains attributes for the assembly time, as well as the
    time it takes to transfer to the next station on a different line.
    """
    def __init__(self, assembly_time, transfer_time=None):
        self.assembly_time = assembly_time
        self.transfer_time = transfer_time

    def __str__(self):
        """ The string representation of the assembly time on this station.
        """
        return str(self.assembly_time)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Finds the fastest way through a factory')
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--print-stations', action='store_true', help='print stations')
    args = parser.parse_args()
    als = AssemblyLineScheduler.read_assembly_lines(args.infile)
    als.fastest_way()
    # printing output...
    if args.print_stations:
        # print stations
        for j in range(als.num_stations):
            print "line %d, station %d" % (als.print_stations_in_order(j), j + 1,)
    else:
        # print results
        print als
        # print out fastest times
        f1, f2 = "", ""
        for i in range(als.num_stations):
            f1 += str(als.assembly_lines[0].fastest_times[i]).ljust(10)
            f2 += str(als.assembly_lines[1].fastest_times[i]).ljust(10)
        print "j".ljust(10) + "".join(map(lambda x: str(x).ljust(10), range(1, als.num_stations + 1)))
        print "f1[j]".ljust(10) + f1
        print "f2[j]".ljust(10) + f2
        print "f* = %d\n" % als.fastest_time
        # print out fastest lines
        l1, l2 = "", ""
        for i in range(als.num_stations - 1):
            l1 += str(als.assembly_lines[0].fastest_lines[i]).ljust(10)
            l2 += str(als.assembly_lines[1].fastest_lines[i]).ljust(10)
        print "j".ljust(10) + "".join(map(lambda x: str(x).ljust(10), range(2, als.num_stations + 1)))
        print "l1[j]".ljust(10) + l1
        print "l2[j]".ljust(10) + l2
        print "l* = %d\n" % als.fastest_line